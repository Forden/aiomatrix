from .. import models
from ..utils import raw_api


class CapabilitiesAPI:
    def __init__(self, raw_api_client: raw_api.RawAPI):
        self._raw_api = raw_api_client

    async def get_server_capabilities(self) -> models.LoginTypes:
        r = await self._raw_api.make_request('GET', '_matrix/client/r0/capabilities', models.ServerCapabilitiesResponse)
        return r
