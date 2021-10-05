from typing import Optional

import pydantic

from ..primitives import UserID


class WhoAmIResponse(pydantic.BaseModel):
    user_id: UserID
    device_id: Optional[str]
