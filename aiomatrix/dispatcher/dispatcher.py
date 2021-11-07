import asyncio
import time
from typing import Callable, List, Union

import pydantic

from .filters import BaseFilter
from .observers import MatrixEventsObserver
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
        self._clients: List[AiomatrixClient] = clients
        self._state_observer: MatrixEventsObserver = MatrixEventsObserver()
        self._generic_observer: MatrixEventsObserver = MatrixEventsObserver()
        self._redaction_observer: MatrixEventsObserver = MatrixEventsObserver()
        self._lock = asyncio.Lock()

    def register_state_handler(
            self, callback: Callable, *filters: BaseFilter
    ):
        self._state_observer.register(callback, *filters)

    def register_generic_handler(
            self, callback: Callable, *filters: BaseFilter
    ):
        self._generic_observer.register(callback, *filters)

    def register_message_handler(
            self, callback: Callable, *filters: BaseFilter
    ):
        from .filters import builtin
        self._generic_observer.register(
            callback,
            builtin.Incoming(),
            builtin.EventType(event_types=[types.misc.RoomEventTypesEnum.room_message]),
            builtin.MessageType(msg_type=[types.misc.RoomMessageEventMsgTypesEnum.text]),
            *filters
        )

    def register_edited_message_handler(
            self, callback: Callable, *filters: BaseFilter
    ):
        from .filters import builtin
        self._generic_observer.register(
            callback,
            builtin.Incoming(),
            builtin.EventType(event_types=[types.misc.RoomEventTypesEnum.room_message]),
            builtin.MessageType(msg_type=[types.misc.RoomMessageEventMsgTypesEnum.text]),
            builtin.IsEditedMessage(is_edited=True),
            *filters
        )

    def register_redaction_handler(
            self, callback: Callable, *filters: BaseFilter
    ):
        from .filters import builtin
        self._redaction_observer.register(
            callback,
            builtin.EventType([types.misc.RoomEventTypesEnum.redaction]),
            *filters
        )

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

    @staticmethod
    def _parse_event(
            event: Union[types.events.RoomEvent, types.events.RoomStateEvent],
            ignore_errors: bool = True
    ) -> Union[types.events.RoomEvent, types.events.RoomMessageEvent, types.events.RoomStateEvent]:
        if isinstance(event, types.events.RoomEvent):
            # if event.unsigned.redacted_because is not None:
            #     # dirty hack to get to original event filed names
            #     event = types.events.RoomRedactionEvent(**json.loads(event.json(by_alias=True)))
            #     event.unsigned.redacted_because = test_types.events.RoomRedactionEvent(**event.unsigned.redacted_because)
            #     return event
            if event.type == types.misc.RoomEventTypesEnum.room_message:
                if event.content is not None:
                    try:
                        event = types.events.RoomMessageEvent.parse_obj(event.dict(by_alias=True))
                    except pydantic.ValidationError as e:
                        if ignore_errors:
                            return event
                        raise e
                    else:
                        return event
            elif event.type == types.misc.RoomEventTypesEnum.reaction:
                if event.content:
                    event.content = types.events.relationships.ReactionRelationshipContent.parse_obj(event.content)
        elif isinstance(event, types.events.RoomStateEvent):
            log.debug(f'received state event: {event}')
        return event

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
                            parsed_events.append(self._parse_event(event))
                    for event in room_data.timeline.events:
                        event.room_id = room_id
                        parsed_events.append(self._parse_event(event))
                    for event in parsed_events:
                        if isinstance(event, types.events.RoomStateEvent):
                            await self._state_observer.trigger(event, client)
                        elif any(isinstance(event, i) for i in [types.events.RoomEvent, types.events.RoomMessageEvent]):
                            if event.type != types.misc.RoomEventTypesEnum.redaction:
                                await self._generic_observer.trigger(event, client)
                            else:
                                await self._redaction_observer.trigger(event, client)
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
