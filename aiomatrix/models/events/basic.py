import datetime
from enum import Enum
from typing import Any, Optional

import pydantic


class BasicEvent(pydantic.BaseModel):
    content: dict
    type: str


class UnsignedData(pydantic.BaseModel):
    age: Optional[int]
    redacted_because: Optional[BasicEvent]
    transcation_id: Optional[str]


class RoomEvent(BasicEvent):
    event_id: str
    sender: str
    origin_server_ts: datetime.datetime
    unsigned: Optional[UnsignedData]
    room_id: Optional[str]  # None only in /sync


class RoomStateEvent(RoomEvent):
    state_key: str
    prev_content: Optional[Any]


class Event(BasicEvent):
    sender: str


class StrippedState(Event):
    state_key: str


class RoomMessageEventMsgTypesEnum(str, Enum):
    text = 'm.text'
    emote = 'm.emote'
    notice = 'm.notice'
    image = 'm.image'
    file = 'm.file'
    audio = 'm.audio'
    location = 'm.location'
    video = 'm.video'


class BasicRoomMessageEventContent(pydantic.BaseModel):
    body: str
    msgtype: str


class RoomMessageEvent(RoomEvent):
    content: BasicRoomMessageEventContent
