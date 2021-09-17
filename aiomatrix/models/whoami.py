from typing import Optional

import pydantic


class WhoAmI(pydantic.BaseModel):
    user_id: str
    device_id: Optional[str]
