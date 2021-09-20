import asyncio
import pathlib
import time
from typing import Dict, Optional, Tuple, Union

from . import apis
from .utils import exceptions, raw_api, storage


class Aiomatrix:
    room_states: Dict[str, list] = {}  # move to db

    def __init__(self, server_url: str, auth_details: Tuple[str, dict], db_path: Union[pathlib.Path, str]):
        self.server_url = server_url
        self.state_db = storage.StateStorage(db_path)
        self.presence_db = storage.PresenceStorage(db_path)
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
                if state.rooms:
                    if state.rooms.join:
                        for room_id in state.rooms.join:
                            room_data = state.rooms.join[room_id]
                            if room_data.state.events:
                                events_in_db = await self.state_db.get_events_batch_data(
                                    [i.event_id for i in room_data.state.events], only_ids=True
                                )
                                for i in room_data.state.events:
                                    i.room_id = room_id
                                await self.state_db.insert_new_events_batch(
                                    [
                                        i for i in
                                        filter(lambda x: x.event_id not in events_in_db, room_data.state.events)
                                    ]
                                )
                if track_presence:
                    if state.presence:
                        for event in state.presence.events:
                            await self.presence_db.add_new_presence_update(event)
                    unupdated_users = await self.presence_db.get_unupdated_users(600)
                    for user in unupdated_users:
                        try:
                            user_presence = await self.presence_api.get_user_presence(user.user_id)
                        except exceptions.Forbidden:
                            print(f'couldn\'t get presence status for {user.user_id}: forbidden')
                        except Exception as e:
                            print(f'error getting presence status: {e=}')
                        else:
                            await self.presence_db.update_user_presence(user.user_id, user_presence)
                print(f'proceeded in {time.time() - t}')
            await asyncio.sleep(sleep)

    async def login_by_password(self, login: str, password: str, device_id: Optional[str] = None):
        supported_login_types = await self.auth_api.get_login_types()
        support_password_auth = 'm.login.password' in map(lambda x: x.type, supported_login_types.flows)
        if support_password_auth:
            login_response = await self.auth_api.password_login(login, password, device_id)
            if login_response.access_token:
                self.auth_api.set_access_token(login_response.access_token)
