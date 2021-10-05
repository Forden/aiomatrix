from enum import Enum
from typing import Optional

import pydantic

from ..base import RoomStateEvent


class RoomMemberMembershipEnum(str, Enum):
    invite = 'invite'
    join = 'join'
    knock = 'knock'
    leave = 'leave'
    ban = 'ban'


class RoomMemberInvite(pydantic.BaseModel):
    display_name: str
    signed: dict


class RoomMemberUnsignedData(pydantic.BaseModel):
    invite_room_state: dict


class RoomMemberContent(pydantic.BaseModel):
    avatar_url: Optional[str]
    displayname: Optional[str]
    membership: RoomMemberMembershipEnum
    is_direct: bool
    third_party_invite: RoomMemberInvite
    unsigned: RoomMemberUnsignedData


class RoomMemberEvent(RoomStateEvent):
    content: RoomMemberContent
