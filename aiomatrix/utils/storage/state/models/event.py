import datetime
from typing import Optional

import pydantic

from aiomatrix import types


class StateEventInDB(pydantic.BaseModel):
    event_id: str
    room_id: Optional[types.primitives.RoomID]
    sender: types.primitives.UserID
    ts: datetime.datetime
    data: types.events.RoomStateEvent
