from typing import List

import pydantic


class ResolveRoomAliasResponse(pydantic.BaseModel):
    room_id: str
    servers: List[str]


class GetRoomAliasesResponse(pydantic.BaseModel):
    aliases: List[str]
