import datetime
from typing import Optional, Union

from pydantic import BaseModel, Field

from .base import MatrixObject
from .room_state_events import RoomStateContent
from .. import primitives
from ..misc import RoomMessageEventMsgTypesEnum
from ...utils.mixins import ContextClientMixin


class BasicEvent(MatrixObject):
    content: primitives.EventContent
    type: str


class UnsignedData(BaseModel):
    age: Optional[int]
    redacted_because: Optional[dict]  # exists if event was redacted while client was offline
    transcation_id: Optional[str]


class RoomEvent(BasicEvent, ContextClientMixin):
    event_id: primitives.EventID
    sender: primitives.UserID
    timestamp: datetime.datetime = Field(..., alias='origin_server_ts')
    redacts: Optional[primitives.EventID]
    unsigned: Optional[UnsignedData]
    room_id: Optional[primitives.RoomID]  # None only in /sync


class RoomStateEvent(RoomEvent):
    content: RoomStateContent
    state_key: str
    prev_content: Optional[primitives.EventContent]


class RelationshipToEventData(MatrixObject):
    rel_type: str  # add enum for realtionship test_types
    event_id: primitives.EventID


class ReplyToRelationshipData(MatrixObject):
    event_id: primitives.EventID


class ReplyToData(MatrixObject):
    reply_data: ReplyToRelationshipData = Field(..., alias='m.in_reply_to')


class RelationshipMixin(MatrixObject):
    relationship: Optional[Union[RelationshipToEventData, ReplyToData]] = Field(None, alias='m.relates_to')


class BaseMessageEventContent(MatrixObject):
    body: Optional[str]
    msgtype: Union[RoomMessageEventMsgTypesEnum, str]
