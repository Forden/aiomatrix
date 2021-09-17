from enum import Enum

import pydantic

from ..basic import StateEvent


class RoomJoinRuleEnum(str, Enum):
    public = 'public'
    knock = 'knock'
    invite = 'invite'
    private = 'private'


class RoomJoinRulesContent(pydantic.BaseModel):
    join_rule: RoomJoinRuleEnum


class RoomJoinRules(StateEvent):
    content: RoomJoinRulesContent
