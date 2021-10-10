import datetime
from typing import Optional, Union

import pydantic
from pydantic import Field

from .. import misc, primitives


class EventObject(pydantic.BaseModel):
    raw: Optional[dict]

    class Config:
        json_encoders = {datetime.datetime: lambda dt: int(dt.timestamp())}

    def __init__(self, **data):
        super().__init__(**data)
        self.raw = data


class BasicEvent(EventObject):
    content: primitives.EventContent
    type: str


class UnsignedData(pydantic.BaseModel):
    age: Optional[int]
    redacted_because: Optional[dict]  # exists if event was redacted while client was offline
    transcation_id: Optional[str]


class RoomEvent(BasicEvent):
    event_id: primitives.EventID
    sender: primitives.UserID
    timestamp: datetime.datetime = Field(..., alias='origin_server_ts')
    redacts: Optional[str]
    unsigned: Optional[UnsignedData]
    room_id: Optional[primitives.RoomID]  # None only in /sync


class RoomStateEvent(RoomEvent):
    state_key: str
    prev_content: Optional[primitives.EventContent]


class Event(BasicEvent):
    sender: primitives.UserID


class StrippedStateEvent(Event):
    state_key: str


class BasicRoomMessageEventContent(EventObject):
    body: str
    msgtype: Union[misc.RoomMessageEventMsgTypesEnum, str]


class BasicRelationshipData(EventObject):
    rel_type: str  # add enum for realtionship types
    event_id: primitives.EventID


class BasicRelationEventContent(EventObject):
    relationship: BasicRelationshipData = pydantic.Field(..., alias='m.relates_to')


class RoomMessageEvent(RoomEvent):
    content: BasicRoomMessageEventContent
