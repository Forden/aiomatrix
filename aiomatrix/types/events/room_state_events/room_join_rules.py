from enum import Enum

import pydantic


class RoomJoinRuleEnum(str, Enum):
    public = 'public'
    knock = 'knock'
    invite = 'invite'
    private = 'private'


class RoomJoinRulesContent(pydantic.BaseModel):
    join_rule: RoomJoinRuleEnum


# class RoomJoinRules(RoomStateEvent):
#     content: RoomJoinRulesContent
