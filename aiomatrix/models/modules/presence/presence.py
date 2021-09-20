from enum import Enum
from typing import Optional

import pydantic


class PresenceEnum(str, Enum):
    offline = 'offline'
    online = 'online'
    unavailable = 'unavailable'


class PresenceEventContent(pydantic.BaseModel):
    avatar_url: Optional[str]
    displayname: Optional[str]
    last_active_ago: int
    presence: PresenceEnum
    currently_active: Optional[bool]
    status_msg: Optional[str]


class CurrentPresenceStatus(pydantic.BaseModel):
    presence: PresenceEnum
    last_active_ago: int
    status_msg: Optional[str]
    currently_active: Optional[bool]


class PresenceEvent(pydantic.BaseModel):
    content: PresenceEventContent
    sender: str
    type: str
