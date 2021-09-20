import asyncio
import datetime
from typing import Dict, Optional, Tuple

from . import apis
from .utils import raw_api


class Aiomatrix:
    room_states: Dict[str, list] = {}  # move to db
    presence: Dict[str, dict] = {}  # move to db

    def __init__(self, server_url: str, auth_details: Tuple[str, dict]):
        self.server_url = server_url
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

    async def run(self, ignore_errors: bool = True, timeout: int = 10, sleep: float = 0.1):
        if not self._raw_api.is_authorized:
            await self._auth_cb(**self._auth_details)
        state = None
        while True:
            try:
                state = await self.sync_api.sync(  # move to function
                    full_state=False,
                    since=state.next_batch if state is not None else None,
                    timeout=timeout * 1000
                )
                if state.rooms:
                    for room_id in state.rooms.join:
                        room_data = state.rooms.join[room_id]
                        if room_id not in self.room_states:
                            self.room_states[room_id] = []
                        self.room_states[room_id].extend(room_data.state.events)
                if state.presence:
                    for event in state.presence.events:
                        now = datetime.datetime.utcnow()
                        self.presence[event.sender] = {
                            'last_active_ago': datetime.datetime.fromtimestamp(
                                now.timestamp() - event.content.last_active_ago
                            ).isoformat(),
                            'status':          event.content.presence,
                            'last_update':     now.isoformat()
                        }
                for user_id in self.presence:
                    now = datetime.datetime.utcnow()
                    if now - datetime.datetime.fromisoformat(
                            self.presence[user_id]['last_update']
                    ) > datetime.timedelta(seconds=60):
                        user_presence = await self.presence_api.get_user_presence(user_id)
                        self.presence[user_id]['last_active_ago'] = datetime.datetime.fromtimestamp(
                            now.timestamp() - user_presence.last_active_ago
                        ).isoformat()
                        self.presence[user_id]['status'] = user_presence.presence
                        self.presence[user_id]['last_update'] = now.isoformat()
            except Exception as e:
                print(e)
                if not ignore_errors:
                    break
            await asyncio.sleep(sleep)

    async def login_by_password(self, login: str, password: str, device_id: Optional[str] = None):
        supported_login_types = await self.auth_api.get_login_types()
        support_password_auth = 'm.login.password' in map(lambda x: x.type, supported_login_types.flows)
        if support_password_auth:
            login_response = await self.auth_api.password_login(login, password, device_id)
            if login_response.access_token:
                self.auth_api.set_access_token(login_response.access_token)
