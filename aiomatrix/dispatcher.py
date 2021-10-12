import asyncio
import time
import typing

from . import exceptions, handlers, types
from .client import AiomatrixClient
from .utils import storage


def _clear_filters(filters: typing.List[handlers.filters.BaseFilter]) -> typing.List[handlers.filters.BaseFilter]:
    """
    removing repeating filters from list
    """
    result = {}
    for i in filters:
        result[i.filter_id] = i
    return list(result.values())


class AiomatrixDispatcher:
    def __init__(self, clients: typing.List[AiomatrixClient], data_storage: storage.StorageRepo):
        self.storage: storage.StorageRepo = data_storage
        self._clients: list[AiomatrixClient] = clients
        self._handlers = []
        self._redaction_handlers = []
        self._lock = asyncio.Lock()

    def register_generic_handler(
            self, callback: typing.Callable, filters: typing.Optional[typing.List[handlers.filters.BaseFilter]] = None
    ):
        if filters is None:
            filters = []
        filters = _clear_filters(filters)
        self._handlers.append(handlers.Handler(callback=callback, filters=filters))

    def register_message_handler(
            self, callback: typing.Callable, filters: typing.Optional[typing.List[handlers.filters.BaseFilter]] = None
    ):
        handler_filters = [
            handlers.filters.builtin.Incoming(),
            handlers.filters.builtin.EventType(event_types=[types.misc.RoomEventTypesEnum.room_message]),
            handlers.filters.builtin.MessageType(msg_type=[types.misc.RoomMessageEventMsgTypesEnum.text])
        ]
        if filters is None:
            filters = []
        handler_filters.extend(filters)
        filters = _clear_filters(handler_filters)
        self._handlers.append(handlers.Handler(callback=callback, filters=filters))

    def register_redaction_handler(
            self, callback: typing.Callable, filters: typing.Optional[typing.List[handlers.filters.BaseFilter]] = None
    ):
        handler_filters = [handlers.filters.builtin.EventType([types.misc.RoomEventTypesEnum.redaction])]
        if filters is None:
            filters = []
        handler_filters.extend(filters)
        filters = _clear_filters(handler_filters)
        self._redaction_handlers.append(handlers.Handler(callback=callback, filters=filters))

    async def _save_events_in_db(self, client: AiomatrixClient, events: typing.List[types.events.RoomEvent]):
        batch_size = 500
        parts = [
            events[i:i + batch_size] for i in range(
                0, len(events), batch_size
            )
        ]
        for i, part in enumerate(parts):
            events_in_db = await self.storage.events_repo.are_new_events(
                client.me, list(map(lambda x: x.event_id, part))
            )
            await self.storage.events_repo.insert_new_events_batch(
                client.me, list(filter(lambda x: not events_in_db[x.event_id], part))
            )

    async def process_sync(
            self, client: AiomatrixClient, state: types.responses.SyncResponse, process_joined_rooms: bool = True,
            process_invited_rooms: bool = True, process_left_rooms: bool = True, process_presence: bool = False
    ):
        """
        main entry point for events to be processed
        :param client:
        :param state:
        :param process_joined_rooms:
        :param process_invited_rooms:
        :param process_left_rooms:
        :param process_presence:
        :return:
        """
        if state.rooms:
            if process_joined_rooms and state.rooms.join:
                for room_id in state.rooms.join:
                    room_data = state.rooms.join[room_id]
                    if room_data.state.events:
                        for event in room_data.state.events:
                            event.room_id = room_id
                        await self._save_events_in_db(client, room_data.state.events)
                for room_id in state.rooms.join:
                    room_data = state.rooms.join[room_id]
                    parsed_events = []
                    for event in room_data.timeline.events:
                        event.room_id = room_id
                        parsed_events.append(client.parse_event(event))
                    for event in parsed_events:
                        kwargs = {'client': client}
                        for handler in self._redaction_handlers:
                            if await handler.check(event, client):
                                await handler.callback(event, **kwargs)
                                break
                        if event.type != types.misc.RoomEventTypesEnum.redaction:
                            kwargs['content'] = event.content
                            for handler in self._handlers:
                                if await handler.check(event, client):
                                    await handler.callback(event, **kwargs)
                                    break
                    await self._save_events_in_db(client, room_data.timeline.events)
            if process_invited_rooms:
                if state.rooms.invite:
                    print(f'{state.rooms.invite=}')
            if process_left_rooms:
                if state.rooms.leave:
                    print(f'{state.rooms.leave=}')
        if process_presence:
            if state.presence:
                for event in state.presence.events:
                    await self.storage.presence_storage.add_new_presence_update(client.me, event)
            unupdated_users = await self.storage.presence_storage.get_outdated_users_data(client.me, 600)
            for user in unupdated_users:
                try:
                    user_presence = await client.presence_api.get_user_presence(user.user_id)
                except exceptions.Forbidden:
                    print(f'couldn\'t get presence status for {user.user_id}: forbidden')
                except Exception as e:
                    print(f'error getting presence status: {e=}')
                else:
                    await self.storage.presence_storage.update_user_presence(client.me, user.user_id, user_presence)

    async def run_polling(
            self, ignore_errors: bool = True, timeout: int = 10, sleep: float = 0.1, track_presence: bool = False
    ):
        async with self._lock:  # to prevent multiple pollings
            coro_list = []
            for i in self._clients:
                coro_list.append(
                    self._run_bot_polling(i, ignore_errors, timeout, sleep, track_presence)
                )
            await asyncio.gather(*coro_list)

    async def _run_bot_polling(
            self, client: AiomatrixClient, ignore_errors: bool = True, timeout: int = 10,
            sleep: float = 0.1, track_presence: bool = False
    ):
        while True:
            await client.login()
            next_batch = await self.storage.internal_repo.get_last_sync_token(client.me)
            try:
                state = await client.sync_api.sync(
                    full_state=False,
                    since=next_batch,
                    timeout=timeout * 1000
                )
            except Exception as e:
                print(f'sync error {e=} for client {client.me}')
                if not ignore_errors:
                    raise e
            else:
                t = time.time()
                await self.process_sync(client, state, process_joined_rooms=True, process_presence=track_presence)
                print(f'sync for client {client.me} proceeded in {time.time() - t}')
                await self.storage.internal_repo.set_last_sync_token(client.me, state.next_batch)
            finally:
                await asyncio.sleep(sleep)
