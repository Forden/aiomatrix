import asyncio
import time
import typing
from typing import Optional, Tuple

from . import apis, handlers, models
from .utils import exceptions, raw_api, storage


class Aiomatrix:
    def __init__(self, server_url: str, auth_details: Tuple[str, dict], data_storage: storage.StorageRepo):
        self.server_url = server_url
        self.storage = data_storage
        self._auth_cb = {'password': self.login_by_password}[auth_details[0]]
        self._auth_details = auth_details[1]
        self._raw_api = raw_api.RawAPI(self.server_url)
        self.auth_api = apis.AuthAPI(self._raw_api)
        self.capabilities_api = apis.CapabilitiesAPI(self._raw_api)
        self.room_api = apis.RoomsAPI(self._raw_api)
        self.room_membership_api = apis.RoomMembershipAPI(self._raw_api)
        self.listing_room_api = apis.ListingRoomsAPI(self._raw_api)
        self.sync_api = apis.SyncingAPI(self._raw_api)
        self.presence_api = apis.modules.PresenceAPI(self._raw_api)

        self._handlers: typing.List[handlers.Handler] = []

    def register_handler(
            self, callback: typing.Callable, filters: typing.Optional[typing.List[handlers.BaseFilter]] = None
    ):
        self._handlers.append(handlers.Handler(callback=callback, filters=filters))

    @staticmethod
    def parse_event(event: models.events.RoomEvent) -> models.events.RoomEvent:
        if event.type == 'm.room.message':
            message_event_content = models.events.BasicRoomMessageEventContent(**event.content)
            msgtypes = {
                models.events.RoomMessageEventMsgTypesEnum.audio:    models.modules.instant_messaging.Audio,
                models.events.RoomMessageEventMsgTypesEnum.emote:    models.modules.instant_messaging.Emote,
                models.events.RoomMessageEventMsgTypesEnum.file:     models.modules.instant_messaging.File,
                models.events.RoomMessageEventMsgTypesEnum.image:    models.modules.instant_messaging.Image,
                models.events.RoomMessageEventMsgTypesEnum.location: models.modules.instant_messaging.Location,
                models.events.RoomMessageEventMsgTypesEnum.notice:   models.modules.instant_messaging.Notice,
                models.events.RoomMessageEventMsgTypesEnum.text:     models.modules.instant_messaging.Text,
                models.events.RoomMessageEventMsgTypesEnum.video:    models.modules.instant_messaging.Video,
            }
            if message_event_content.msgtype in msgtypes:
                event.content = msgtypes[message_event_content.msgtype](**event.content)
        return event

    async def login(self):
        if not self._raw_api.is_authorized:
            await self._auth_cb(**self._auth_details)

    async def process_sync(
            self, state: models.SyncResponse, process_joined_rooms: bool = True, process_invited_rooms: bool = True,
            process_left_rooms: bool = True, process_presence: bool = False
    ):
        if state.rooms:
            if process_joined_rooms:
                if state.rooms.join:
                    for room_id in state.rooms.join:
                        room_data = state.rooms.join[room_id]
                        if room_data.state.events:
                            batch_size = 500
                            parts = [
                                room_data.state.events[i:i + batch_size] for i in range(
                                    0, len(room_data.state.events), batch_size
                                )
                            ]
                            for i, part in enumerate(parts):
                                print(f'processing {len(part)} events from {i}/{len(parts)} part')
                                events_in_db = await self.storage.state_repo.are_new_events(
                                    list(map(lambda x: x.event_id, part))
                                )
                                for event in part:
                                    event.room_id = room_id
                                await self.storage.state_repo.insert_new_events_batch(
                                    list(filter(lambda x: not events_in_db[x.event_id], part))
                                )
                    for room_id in state.rooms.join:
                        room_data = state.rooms.join[room_id]
                        parsed_events = []
                        for event in room_data.timeline.events:
                            event.room_id = room_id
                            parsed_events.append(self.parse_event(event))
                        for event in parsed_events:
                            for handler in self._handlers:
                                if await handler.check(event):
                                    await handler.callback(event)
                                    break
            if process_invited_rooms:
                if state.rooms.invite:
                    print(f'{state.rooms.invite=}')
            if process_left_rooms:
                if state.rooms.leave:
                    print(f'{state.rooms.leave=}')
        if process_presence:
            if state.presence:
                for event in state.presence.events:
                    await self.storage.presence_storage.add_new_presence_update(event)
            unupdated_users = await self.storage.presence_storage.get_outdated_users_data(600)
            for user in unupdated_users:
                try:
                    user_presence = await self.presence_api.get_user_presence(user.user_id)
                except exceptions.Forbidden:
                    print(f'couldn\'t get presence status for {user.user_id}: forbidden')
                except Exception as e:
                    print(f'error getting presence status: {e=}')
                else:
                    await self.storage.presence_storage.update_user_presence(user.user_id, user_presence)

    async def run(
            self, ignore_errors: bool = True, timeout: int = 10, sleep: float = 0.1, track_presence: bool = False
    ):
        await self.login()
        while True:
            next_batch = await self.storage.internal_repo.get_last_sync_token()
            try:
                state = await self.sync_api.sync(
                    full_state=False,
                    since=next_batch,
                    timeout=timeout * 1000
                )
            except Exception as e:
                print(f'sync error {e=}')
                if not ignore_errors:
                    raise e
            else:
                t = time.time()
                await self.process_sync(state, process_joined_rooms=True, process_presence=track_presence)
                print(f'proceeded in {time.time() - t}')
                await self.storage.internal_repo.set_last_sync_token(state.next_batch)
            await asyncio.sleep(sleep)

    async def login_by_password(self, login: str, password: str, device_id: Optional[str] = None):
        supported_login_types = await self.auth_api.get_login_types()
        support_password_auth = 'm.login.password' in map(lambda x: x.type, supported_login_types.flows)
        if support_password_auth:
            login_response = await self.auth_api.password_login(login, password, device_id)
            if login_response.access_token:
                self.auth_api.set_access_token(login_response.access_token)
