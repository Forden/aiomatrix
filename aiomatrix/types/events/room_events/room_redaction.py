from typing import Optional

import pydantic

from ..base import RoomEvent


class RoomRedactionContent(pydantic.BaseModel):
    reason: Optional[str]


class RoomRedactionEvent(RoomEvent):  # redaction of already sent event
    content: RoomRedactionContent
