from typing import Optional

import pydantic
from pydantic import Field

from ... import primitives


class PreviousRoom(pydantic.BaseModel):
    room_id: primitives.RoomID
    event_id: primitives.EventID


class RoomCreateContent(pydantic.BaseModel):
    creator: primitives.UserID
    federate: bool = Field(True, alias='m.federate')
    room_version: str = '1'
    predecessor: Optional[PreviousRoom]


# class RoomCreate(RoomStateEvent):
#     content: RoomCreateContent
