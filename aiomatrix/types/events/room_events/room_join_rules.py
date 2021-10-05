from enum import Enum

import pydantic

from ..base import RoomStateEvent


class RoomJoinRuleEnum(str, Enum):
    public = 'public'
    knock = 'knock'
    invite = 'invite'
    private = 'private'


class RoomJoinRulesContent(pydantic.BaseModel):
    join_rule: RoomJoinRuleEnum


class RoomJoinRules(RoomStateEvent):
    content: RoomJoinRulesContent
