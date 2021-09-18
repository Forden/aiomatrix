from enum import Enum
from typing import Any

import pydantic


class RoomVisiblityEnum(str, Enum):
    public = 'public'
    private = 'private'


class CreateRoomPresetEnum(str, Enum):
    public_chat = 'public_chat'
    private_chat = 'private_chat'
    trusted_private_chat = 'trusted_private_chat'


class CreateRoomStateEvent(pydantic.BaseModel):
    type: str
    state_key: str = ''
    content: Any


class CreateRoomInvite3PID(pydantic.BaseModel):
    id_server: str
    id_access_token: str
    medium: str
    address: str


class CreateRoomResponse(pydantic.BaseModel):
    room_id: str
    room_alias: str
