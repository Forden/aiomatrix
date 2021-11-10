import typing
from typing import Optional, Tuple

from . import apis
from .apis import raw_api
from .. import types
from ..utils.mixins import ContextVarMixin


class AiomatrixClient(ContextVarMixin):
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
        self.instant_messaging_api = apis.modules.InstantMessagingAPI(self.sync_api)
        self.typing_notifications_api = apis.modules.TypingNotifications(self._raw_api)
        self.content_repository_api = apis.modules.ContentRepositoryAPI(self._raw_api)

        self.me: typing.Optional[types.responses.WhoAmIResponse] = None

    async def login(self):
        if not self._raw_api.is_authorized:
            login_result = await self._auth_cb(**self._auth_details)
            if login_result:
                self.me = await self.auth_api.whoami()

    async def login_by_password(self, login: str, password: str, device_id: Optional[str] = None) -> bool:
        supported_login_types = await self.auth_api.get_login_types()
        support_password_auth = 'm.login.password' in map(lambda x: x.type, supported_login_types.flows)
        if support_password_auth:
            login_response = await self.auth_api.password_login(login, password, device_id)
            if login_response.access_token:
                self.auth_api.set_access_token(login_response.access_token)
                return True
        return False
