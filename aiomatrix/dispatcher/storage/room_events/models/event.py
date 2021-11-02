import datetime
from typing import Optional

import pydantic

from aiomatrix import types


class EventInDB(pydantic.BaseModel):
    account_id: types.primitives.UserID
    event_id: types.primitives.EventID
    relates_to: Optional[types.primitives.EventID]
    event_type: str
    room_id: Optional[types.primitives.RoomID]
    sender: types.primitives.UserID
    ts: datetime.datetime
    data: types.events.RoomEvent


class SeenEvent(pydantic.BaseModel):
    account_id: types.primitives.UserID
    event_id: types.primitives.EventID
