from typing import List, Optional

import pydantic

from ..basic import StateEvent


class RoomCanonicalAliasContent(pydantic.BaseModel):
    alias: Optional[str]
    alt_aliases: Optional[List[str]]


class RoomCanonicalAlias(StateEvent):
    content: RoomCanonicalAliasContent
