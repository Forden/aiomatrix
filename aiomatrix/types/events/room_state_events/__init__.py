from typing import Union

from .room_canonical_alias import RoomCanonicalAliasContent
from .room_create import RoomCreateContent
from .room_join_rules import RoomJoinRuleEnum, RoomJoinRulesContent
from .room_member import RoomMemberContent, RoomMemberMembershipEnum
from .room_power_levels import RoomPowerLevelContent
from .room_redaction import RoomRedactionContent

RoomStateContent = Union[
    RoomCanonicalAliasContent, RoomCreateContent, RoomJoinRulesContent, RoomMemberContent, RoomPowerLevelContent, RoomRedactionContent
]
