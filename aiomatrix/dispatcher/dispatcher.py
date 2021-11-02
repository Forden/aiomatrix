import asyncio
import time
from typing import Callable, List, Optional

from .filters import BaseFilter
from .handlers import Handler
from .storage import StorageRepo
from .. import exceptions, loggers, types
from ..client import AiomatrixClient

log = loggers.dispatcher


def _clear_filters(filters: List[BaseFilter]) -> List[BaseFilter]:
    """
    removing repeating filters from list
    """
    result = {}
    for i in filters:
        result[i.filter_id] = i
    return list(result.values())


class AiomatrixDispatcher:
    def __init__(self, clients: List[AiomatrixClient], data_storage: StorageRepo):
        self.storage: StorageRepo = data_storage
        self._clients: list[AiomatrixClient] = clients
        self._state_handlers: List[Handler] = []
        self._handlers: List[Handler] = []
        self._redaction_handlers: List[Handler] = []
        self._lock = asyncio.Lock()

    def register_state_handler(
            self, callback: Callable, filters: Optional[List[BaseFilter]] = None
    ):
        if filters is None:
            filters = []
        filters = _clear_filters(filters)
        self._state_handlers.append(Handler(callback=callback, filters=filters))

    def register_generic_handler(
            self, callback: Callable, filters: Optional[List[BaseFilter]] = None
    ):
        if filters is None:
            filters = []
        filters = _clear_filters(filters)
        self._handlers.append(Handler(callback=callback, filters=filters))

    def register_message_handler(
            self, callback: Callable, filters: Optional[List[BaseFilter]] = None
    ):
        from .filters import builtin
        handler_filters = [
            builtin.Incoming(),
            builtin.EventType(event_types=[types.misc.RoomEventTypesEnum.room_message]),
            builtin.MessageType(msg_type=[types.misc.RoomMessageEventMsgTypesEnum.text])
        ]
        if filters is None:
            filters = []
        handler_filters.extend(filters)
        filters = _clear_filters(handler_filters)
        self._handlers.append(Handler(callback=callback, filters=filters))

    def register_redaction_handler(
            self, callback: Callable, filters: Optional[List[BaseFilter]] = None
    ):
        from .filters import builtin
        handler_filters = [
            builtin.EventType([types.misc.RoomEventTypesEnum.redaction])
        ]
        if filters is None:
            filters = []
        handler_filters.extend(filters)
        filters = _clear_filters(handler_filters)
        self._redaction_handlers.append(Handler(callback=callback, filters=filters))

    async def _save_events_in_db(self, client: AiomatrixClient, events: List[types.events.RoomEvent]):
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
        AiomatrixClient.set(client)
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
                    if room_data.state.events:
                        for event in room_data.state.events:
                            event.room_id = room_id
                            parsed_events.append(client.parse_event(event))
                    for event in room_data.timeline.events:
                        event.room_id = room_id
                        parsed_events.append(client.parse_event(event))
                    for event in parsed_events:
                        kwargs = {'client': client}
                        if isinstance(event, types.events.RoomStateEvent):
                            for handler in self._state_handlers:
                                kwargs['content'] = event.content
                                if await handler.check(event, client):
                                    await handler.callback(event, **kwargs)
                                    break
                        elif isinstance(event, types.events.RoomEvent):
                            if event.type != types.misc.RoomEventTypesEnum.redaction:
                                kwargs['content'] = event.content
                                for handler in self._handlers:
                                    if await handler.check(event, client):
                                        await handler.callback(event, **kwargs)
                                        break
                            for handler in self._redaction_handlers:
                                if 'content' in kwargs:
                                    del kwargs['content']
                                if await handler.check(event, client):
                                    await handler.callback(event, **kwargs)
                                    break
                    await self._save_events_in_db(client, room_data.timeline.events)
            if process_invited_rooms:
                if state.rooms.invite:
                    log.debug(f'{state.rooms.invite=}')
            if process_left_rooms:
                if state.rooms.leave:
                    log.debug(f'{state.rooms.leave=}')
        if process_presence:
            if state.presence:
                for event in state.presence.events:
                    await self.storage.presence_storage.add_new_presence_update(client.me, event)
            unupdated_users = await self.storage.presence_storage.get_outdated_users_data(client.me, 600)
            for user in unupdated_users:
                try:
                    user_presence = await client.presence_api.get_user_presence(user.user_id)
                except exceptions.Forbidden:
                    log.error(f'couldn\'t get presence status for {user.user_id}: forbidden')
                except Exception as e:
                    log.exception(f'error getting presence status: {e=}')
                else:
                    await self.storage.presence_storage.update_user_presence(client.me, user.user_id, user_presence)

    async def run_polling(
            self, ignore_errors: bool = True, timeout: int = 10, sleep: float = 0.1, track_presence: bool = False
    ):
        async with self._lock:  # to prevent multiple pollings
            await self.storage.setup()
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
            except (exceptions.MissingToken, exceptions.UnknownToken) as e:
                log.exception(f'login error {e=} for client {client.me}')
                await client.auth_api.logout()
                await client.login()
                if not client.auth_api.is_logged_in:
                    log.exception(f'couldn\'t recover from login error for client {client.me}')
                    break
            except Exception as e:
                log.exception(f'sync error {e=} for client {client.me}')
                if not ignore_errors:
                    raise e
            else:
                t = time.time()
                await self.process_sync(client, state, process_joined_rooms=True, process_presence=track_presence)
                log.debug(f'sync for client {client.me} proceeded in {time.time() - t}')
                await self.storage.internal_repo.set_last_sync_token(client.me, state.next_batch)
            finally:
                await asyncio.sleep(sleep)
