from typing import Any, Optional

import pydantic


class BasicEvent(pydantic.BaseModel):
    content: Any
    type: str


class UnsignedData(pydantic.BaseModel):
    age: int
    redacted_because: Optional[BasicEvent]
    transcation_id: Optional[str]


class RoomEvent(BasicEvent):
    event_id: str
    sender: str
    origin_server_ts: int
    unsigned: Optional[UnsignedData]
    room_id: str


class StateEvent(RoomEvent):
    state_key: str
    prev_content: Optional[Any]
