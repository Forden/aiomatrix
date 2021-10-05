from typing import List, Optional

import pydantic


class DeviceLists(pydantic.BaseModel):
    changed: Optional[List[str]]
    left: Optional[List[str]]
