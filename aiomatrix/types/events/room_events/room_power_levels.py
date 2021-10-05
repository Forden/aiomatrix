from typing import Dict

import pydantic

from ..base import RoomStateEvent


class RoomPowerLevelNotifications(pydantic.BaseModel):
    room: int = 50


class RoomPowerLevelContent(pydantic.BaseModel):
    ban: int = 50
    events: Dict[str, int]
    events_default: int = 0
    invite: int = 50
    kick: int = 50
    redact: int = 50
    state_default: int = 50
    users: Dict[str, int]
    users_default: int = 0
    notifications: RoomPowerLevelNotifications = RoomPowerLevelNotifications()


class RoomPowerLevelEvent(RoomStateEvent):
    content: RoomPowerLevelContent
