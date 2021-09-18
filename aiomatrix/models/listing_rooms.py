from typing import List, Optional

import pydantic

from .create_room import RoomVisiblityEnum


class RoomVisibilityResponse(pydantic.BaseModel):
    visibility: RoomVisiblityEnum


class ServerPublicRoomsChunk(pydantic.BaseModel):
    aliases: List[str] = []
    canonical_alias: Optional[str]
    name: Optional[str]
    num_joined_members: int
    room_id: str
    topic: Optional[str]
    world_readable: bool
    guest_can_join: bool
    avatar_url: Optional[str]


class ServerPublicRoomsResponse(pydantic.BaseModel):
    chunk: List[ServerPublicRoomsChunk]
    next_batch: Optional[str]
    prev_batch: Optional[str]
    total_room_count_estimate: Optional[int]
