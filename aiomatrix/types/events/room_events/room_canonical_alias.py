from typing import List, Optional

import pydantic

from ..base import RoomStateEvent


class RoomCanonicalAliasContent(pydantic.BaseModel):
    alias: Optional[str]
    alt_aliases: Optional[List[str]]


class RoomCanonicalAlias(RoomStateEvent):
    content: RoomCanonicalAliasContent
