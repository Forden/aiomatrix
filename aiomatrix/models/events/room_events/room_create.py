from typing import Optional

import pydantic
from pydantic import Field

from ..basic import RoomStateEvent


class PreviousRoom(pydantic.BaseModel):
    room_id: str
    event_id: str


class RoomCreateContent(pydantic.BaseModel):
    creator: str
    federate: bool = Field(True, alias='m.federate')
    room_version: str = '1'
    predecessor: Optional[PreviousRoom]


class RoomCreate(RoomStateEvent):
    content: RoomCreateContent
