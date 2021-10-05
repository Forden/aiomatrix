from typing import List

import pydantic

from .. import primitives


class ResolveRoomAliasResponse(pydantic.BaseModel):
    room_id: primitives.RoomID
    servers: List[str]


class GetRoomAliasesResponse(pydantic.BaseModel):
    aliases: List[primitives.RoomAlias]
