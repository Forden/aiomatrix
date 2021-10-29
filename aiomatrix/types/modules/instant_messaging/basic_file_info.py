from typing import Optional

from pydantic import BaseModel


class BasicFileInfo(BaseModel):
    mimetype: Optional[str]
    size: int
