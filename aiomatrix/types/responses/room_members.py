from typing import List

import pydantic

from ..events import RoomStateEvent


class RoomMembersResponse(pydantic.BaseModel):
    chunk: List[RoomStateEvent]
