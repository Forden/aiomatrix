import datetime
from typing import Optional, Union

from pydantic import BaseModel, Field

from .base import MatrixEventObject
from .. import primitives


class BasicEvent(MatrixEventObject):
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


class RelationshipToEventData(MatrixEventObject):
    rel_type: str  # add enum for realtionship types
    event_id: primitives.EventID


class ReplyToRelationshipData(MatrixEventObject):
    event_id: primitives.EventID


class ReplyToData(MatrixEventObject):
    reply_data: ReplyToRelationshipData = Field(..., alias='m.in_reply_to')


class RelationshipMixin(MatrixEventObject):
    relationship: Optional[Union[RelationshipToEventData, ReplyToData]] = Field(None, alias='m.relates_to')






