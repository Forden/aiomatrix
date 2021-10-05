from typing import List

import pydantic

from ..events import RoomMemberEvent


class RoomMembersResponse(pydantic.BaseModel):
    chunk: List[RoomMemberEvent]
