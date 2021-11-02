from pydantic import BaseModel

from aiomatrix import types


class RoomInDB(BaseModel):
    room_id: types.primitives.RoomID
    is_encrypted: bool
