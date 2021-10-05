from typing import Optional

import pydantic


class BasicFileInfo(pydantic.BaseModel):
    mimetype: Optional[str]
    size: int
