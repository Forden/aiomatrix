from typing import Optional

from .. import models
from ..utils import raw_api


class SyncingAPI:
    def __init__(self, raw_api_client: raw_api.RawAPI):
        self._raw_api = raw_api_client
        self.state = dict

    async def sync(
            self, filter_id: Optional[str] = None, since: Optional[str] = None, full_state: bool = False,
            set_presence: models.modules.presence.PresenceEnum = models.modules.presence.PresenceEnum.online,
            timeout: int = 0
    ) -> models.SyncResponse:
        payload = {'params': {}}
        if filter_id is not None:
            payload['params']['filter'] = filter_id
        if since is not None:
            payload['params']['since'] = since
        if full_state is not None:
            payload['params']['full_state'] = full_state.__str__().lower()
        if set_presence is not None:
            payload['params']['set_presence'] = f'{set_presence}'
        if timeout is not None:
            payload['params']['timeout'] = timeout
        r = await self._raw_api.make_request(
            'GET', '_matrix/client/r0/sync', models.SyncResponse, **payload
        )
        return r
