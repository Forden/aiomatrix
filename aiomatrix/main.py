import asyncio
import time
from typing import Optional, Tuple

from . import apis, models
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
                                events_in_db = await self.storage.state_storage.get_event_data_batch(
                                    [i.event_id for i in part], only_ids=True
                                )
                                for event in part:
                                    event.room_id = room_id
                                await self.storage.state_storage.insert_new_events_batch(
                                    list(filter(lambda x: x.event_id not in events_in_db, part))
                                )
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
            unupdated_users = await self.storage.presence_storage.get_unupdated_users(600)
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
        state = None
        while True:
            try:
                state = await self.sync_api.sync(  # move to function
                    full_state=False,
                    since=state.next_batch if state is not None else None,
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
            await asyncio.sleep(sleep)

    async def login_by_password(self, login: str, password: str, device_id: Optional[str] = None):
        supported_login_types = await self.auth_api.get_login_types()
        support_password_auth = 'm.login.password' in map(lambda x: x.type, supported_login_types.flows)
        if support_password_auth:
            login_response = await self.auth_api.password_login(login, password, device_id)
            if login_response.access_token:
                self.auth_api.set_access_token(login_response.access_token)
