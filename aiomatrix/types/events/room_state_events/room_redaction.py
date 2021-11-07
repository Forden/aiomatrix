from typing import Optional

import pydantic


class RoomRedactionContent(pydantic.BaseModel):
    reason: Optional[str]


# class RoomRedactionEvent(RoomEvent):  # redaction of already sent event
#     content: RoomRedactionContent
