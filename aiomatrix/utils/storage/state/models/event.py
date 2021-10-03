import datetime
from typing import Optional

import pydantic

from aiomatrix import models


class StateEventInDB(pydantic.BaseModel):
    event_id: str
    room_id: Optional[str]
    sender: str
    ts: datetime.datetime
    data: models.events.RoomStateEvent
