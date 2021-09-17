import pydantic

from ..basic import StateEvent


class RoomRedactionContent(pydantic.BaseModel):
    reason: str


class RoomRedaction(StateEvent):
    content: RoomRedactionContent
