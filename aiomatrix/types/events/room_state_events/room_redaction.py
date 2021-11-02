from typing import Optional

import pydantic

from ..base_room_events import RoomEvent


class RoomRedactionContent(pydantic.BaseModel):
    reason: Optional[str]


class RoomRedactionEvent(RoomEvent):  # redaction of already sent event
    content: RoomRedactionContent
