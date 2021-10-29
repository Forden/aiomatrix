import datetime
from typing import Optional, Union

from pydantic import BaseModel, Field

from .. import misc, primitives


class EventObject(BaseModel):
    raw: Optional[dict]

    class Config:
        json_encoders = {datetime.datetime: lambda dt: int(dt.timestamp())}

    def __init__(self, **data):
        super().__init__(**data)
        self.raw = data


class BasicEvent(EventObject):
    content: primitives.EventContent
    type: str


class UnsignedData(BaseModel):
    age: Optional[int]
    redacted_because: Optional[dict]  # exists if event was redacted while client was offline
    transcation_id: Optional[str]


class RoomEvent(BasicEvent):
    event_id: primitives.EventID
    sender: primitives.UserID
    timestamp: datetime.datetime = Field(..., alias='origin_server_ts')
    redacts: Optional[primitives.EventID]
    unsigned: Optional[UnsignedData]
    room_id: Optional[primitives.RoomID]  # None only in /sync


class RoomStateEvent(RoomEvent):
    state_key: str
    prev_content: Optional[primitives.EventContent]


class RelationshipToEventData(EventObject):
    rel_type: str  # add enum for realtionship types
    event_id: primitives.EventID


class ReplyToRelationshipData(EventObject):
    event_id: primitives.EventID


class ReplyToData(EventObject):
    reply_data: ReplyToRelationshipData = Field(..., alias='m.in_reply_to')


class RelationshipMixin(EventObject):
    relationship: Optional[Union[RelationshipToEventData, ReplyToData]] = Field(None, alias='m.relates_to')


class BasicRoomMessageEventContent(RelationshipMixin):
    body: str
    msgtype: Union[misc.RoomMessageEventMsgTypesEnum, str]
    new_content: 'BasicRoomMessageEventContent' = Field(None, alias='m.new_content')


class RoomMessageEvent(RoomEvent):
    content: BasicRoomMessageEventContent


class Event(BasicEvent):
    sender: primitives.UserID


class StrippedStateEvent(Event):
    state_key: str


BasicRoomMessageEventContent.update_forward_refs()
