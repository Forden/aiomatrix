from typing import List

import pydantic

from ..events import RoomEvent, RoomStateEvent


class RoomMessagesResponse(pydantic.BaseModel):
    start: str
    end: str
    chunk: List[RoomEvent]
    state: List[RoomStateEvent]
