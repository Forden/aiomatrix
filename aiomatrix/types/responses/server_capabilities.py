from typing import Dict

import pydantic
from pydantic import Field

from ..misc import RoomStabilityEnum


class ChangePasswordCapability(pydantic.BaseModel):
    enabled: bool


class RoomVersionsCapability(pydantic.BaseModel):
    default: str
    available: Dict[str, RoomStabilityEnum]


class ServerCapabilities(pydantic.BaseModel):
    change_password: ChangePasswordCapability = Field(None, alias='m.change_password')
    room_versions: RoomVersionsCapability = Field(None, alias='m.room_versions')


class ServerCapabilitiesResponse(pydantic.BaseModel):
    capabilities: ServerCapabilities
