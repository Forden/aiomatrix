from typing import Optional

from .. import models
from ..utils import raw_api


class AuthAPI:
    def __init__(self, raw_api_client: raw_api.RawAPI):
        self._raw_api = raw_api_client

    async def get_login_types(self) -> models.LoginTypes:
        r = await self._raw_api.make_request('GET', '_matrix/client/r0/login', models.LoginTypes)
        return r

    async def password_login(self, login: str, password: str, device_id: Optional[str] = None) -> models.LoginResponse:
        payload = {
            'data': {
                'type':                        'm.login.password',
                'identifier':                  {
                    'type': 'm.id.user',
                    'user': login
                },
                'password':                    password,
                'initial_device_display_name': 'aiomatrix-bot'
            }
        }
        if device_id is not None:
            payload['data']['device_id'] = device_id
        r = await self._raw_api.make_request('POST', '_matrix/client/r0/login', models.LoginResponse, **payload)
        return r

    def set_access_token(self, access_token: str):
        self._raw_api.set_access_token(access_token)

    async def logout(self):
        await self._raw_api.make_request('POST', '_matrix/client/r0/logout')

    async def logout_all(self):
        await self._raw_api.make_request('POST', '_matrix/client/r0/logout/all')

    async def whoami(self) -> models.WhoAmI:
        r = await self._raw_api.make_request('GET', '_matrix/client/r0/account/whoami', models.WhoAmI)
        return r
