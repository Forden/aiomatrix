from . import apis
from .utils import raw_api


class Aiomatrix:
    def __init__(self, server_url: str):
        self._raw_api = raw_api.RawAPI(server_url)
        self.auth_api = apis.AuthAPI(self._raw_api)
        self.capabilities_api = apis.CapabilitiesAPI(self._raw_api)
