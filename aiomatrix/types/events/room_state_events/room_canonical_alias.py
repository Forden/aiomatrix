from typing import List, Optional

import pydantic


class RoomCanonicalAliasContent(pydantic.BaseModel):
    alias: Optional[str]
    alt_aliases: Optional[List[str]]


# class RoomCanonicalAlias(RoomStateEvent):
#     content: RoomCanonicalAliasContent
