import pydantic

from ..basic import RoomStateEvent


class RoomRedactionContent(pydantic.BaseModel):
    reason: str


class RoomRedaction(RoomStateEvent):
    content: RoomRedactionContent
