import pydantic
from pydantic import Field

from ..primitives import UserID


class HomeserverInformation(pydantic.BaseModel):
    base_url: str


class IdentityInformation(pydantic.BaseModel):
    base_url: str


class DiscoveryInformation(pydantic.BaseModel):
    homeserver: HomeserverInformation = Field(..., alias='m.homeserver')
    identity_server: IdentityInformation = Field(None, alias='m.identity_server')


class LoginResponse(pydantic.BaseModel):
    user_id: UserID
    access_token: str
    device_id: str
    well_known: DiscoveryInformation
