from typing import Optional

from .. import models
from ..utils import raw_api


class SyncingAPI:
    def __init__(self, raw_api_client: raw_api.RawAPI):
        self._raw_api = raw_api_client
        self.state = dict

    async def sync(
            self, filter_id: Optional[str] = None, since: Optional[str] = None, full_state: bool = False,
            set_presence: models.SetPresenceEnum = models.SetPresenceEnum.online, timeout: int = 0
    ) -> models.SyncResponse:
        payload = {'data': {}}
        if filter_id is not None:
            payload['data']['filter'] = filter_id
        if since is not None:
            payload['data']['since'] = since
        if full_state is not None:
            payload['data']['full_state'] = full_state
        if set_presence is not None:
            payload['data']['set_presence'] = f'{set_presence}'
        if timeout is not None:
            payload['data']['timeout'] = timeout
        r = await self._raw_api.make_request(
            'GET', '_matrix/client/r0/sync', models.SyncResponse, **payload
        )
        return r
