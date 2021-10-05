from typing import List

import pydantic

from .. import primitives


class UserJoinedRoomsResponse(pydantic.BaseModel):
    joined_rooms: List[primitives.RoomID]


class UserJoinRoomResponse(pydantic.BaseModel):
    room_id: primitives.RoomID
