import datetime
from typing import Optional

import pydantic

from aiomatrix import types


class EventInDB(pydantic.BaseModel):
    account_id: str
    event_id: str
    event_type: str
    room_id: Optional[types.primitives.RoomID]
    sender: types.primitives.UserID
    ts: datetime.datetime
    data: types.events.RoomEvent


class SeenEvent(pydantic.BaseModel):
    account_id: str
    event_id: str
