from typing import List

import pydantic


class DeviceLists(pydantic.BaseModel):
    changed: List[str]
    left: List[str]
