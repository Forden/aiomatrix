from enum import Enum
from typing import Dict

import pydantic
from pydantic import Field


class ChangePasswordCapability(pydantic.BaseModel):
    enabled: bool


class RoomStability(str, Enum):
    stable = 'stable'
    unstable = 'unstable'


class RoomVersionsCapability(pydantic.BaseModel):
    default: str
    available: Dict[str, RoomStability]


class ServerCapabilities(pydantic.BaseModel):
    change_password: ChangePasswordCapability = Field(None, alias='m.change_password')
    room_versions: RoomVersionsCapability = Field(None, alias='m.room_versions')


class ServerCapabilitiesResponse(pydantic.BaseModel):
    capabilities: ServerCapabilities
