import pydantic

from .. import primitives


class CreateRoomResponse(pydantic.BaseModel):
    room_id: primitives.RoomID
    room_alias: primitives.RoomAlias
