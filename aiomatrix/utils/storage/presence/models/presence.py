import datetime
from typing import Optional

import pydantic

from aiomatrix import types


class PresenceInDB(pydantic.BaseModel):
    user_id: types.primitives.UserID
    presence: types.misc.PresenceEnum
    last_active: Optional[datetime.datetime]
    status_msg: Optional[str]
    last_update: datetime.datetime
