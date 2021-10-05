import datetime
from typing import Any, Optional, Union

import pydantic
from pydantic import Field

from .. import misc, primitives


class EventObject(pydantic.BaseModel):
    class Config:
        json_encoders = {datetime.datetime: lambda dt: int(dt.timestamp())}


class BasicEvent(EventObject):
    content: dict
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
    prev_content: Optional[Any]


class Event(BasicEvent):
    sender: primitives.UserID


class StrippedState(Event):
    state_key: str


class BasicRoomMessageEventContent(pydantic.BaseModel):
    body: str
    msgtype: Union[misc.RoomMessageEventMsgTypesEnum, str]


class BasicRelationshipData(pydantic.BaseModel):
    rel_type: str  # add enum for realtionship types
    event_id: primitives.EventID


class BasicRelationEventContent(pydantic.BaseModel):
    relationship: BasicRelationshipData = pydantic.Field(..., alias='m.relates_to')


class RoomMessageEvent(RoomEvent):
    content: BasicRoomMessageEventContent
