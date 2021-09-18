from typing import List

import pydantic


class UserJoinedRoomsResponse(pydantic.BaseModel):
    joined_rooms: List[str]


class UserJoinRoomThirdPartSigned(pydantic.BaseModel):
    sender: str
    mxid: str
    token: str
    signatures: dict


class UserJoinRoomResponse(pydantic.BaseModel):
    room_id: str
