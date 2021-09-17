from typing import Optional

import pydantic


class StandardError(pydantic.BaseModel):
    errcode: str
    error: Optional[str]
