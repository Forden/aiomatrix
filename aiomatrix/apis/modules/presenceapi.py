from typing import Optional

from aiomatrix import models
from aiomatrix.utils import raw_api


class PresenceAPI:
    def __init__(self, raw_api_client: raw_api.RawAPI):
        self._raw_api = raw_api_client

    async def set_user_state(
            self, user_id: str, new_presence: models.modules.presence.PresenceEnum, status_msg: Optional[str] = None
    ):
        payload = {
            'data': {
                'presence': new_presence
            }
        }
        if status_msg is not None:
            payload['data']['status_msg'] = status_msg
        await self._raw_api.make_request(
            'PUT', f'_matrix/client/r0/presence/{user_id}/status', models.modules.presence.CurrentPresenceStatus
        )

    async def get_user_presence(self, user_id: str) -> models.modules.presence.CurrentPresenceStatus:
        r = await self._raw_api.make_request(
            'GET', f'_matrix/client/r0/presence/{user_id}/status', models.modules.presence.CurrentPresenceStatus
        )
        return r
