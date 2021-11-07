from typing import Optional

import pydantic

from aiomatrix.types import misc, primitives


class PresenceEventContent(pydantic.BaseModel):
    avatar_url: Optional[str]
    displayname: Optional[str]
    last_active_ago: Optional[int]
    presence: misc.PresenceEnum
    currently_active: Optional[bool]
    status_msg: Optional[str]


class CurrentPresenceStatus(pydantic.BaseModel):
    presence: misc.PresenceEnum
    last_active_ago: Optional[int]
    status_msg: Optional[str]
    currently_active: Optional[bool]


class PresenceEvent(pydantic.BaseModel):
    content: PresenceEventContent
    sender: primitives.UserID
    type: str
