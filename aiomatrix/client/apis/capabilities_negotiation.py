from aiomatrix import types
from . import raw_api


class CapabilitiesAPI:
    def __init__(self, raw_api_client: raw_api.RawAPI):
        self._raw_api = raw_api_client

    async def get_server_capabilities(self) -> types.responses.ServerCapabilitiesResponse:
        r = await self._raw_api.make_request(
            'GET', '_matrix/client/r0/capabilities', model_type=types.responses.ServerCapabilitiesResponse
        )
        return r
