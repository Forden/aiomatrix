import datetime
from typing import Optional

import pydantic

from aiomatrix import models


class PresenceInDB(pydantic.BaseModel):
    user_id: str
    presence: models.modules.presence.PresenceEnum
    last_active: Optional[datetime.datetime]
    status_msg: Optional[str]
    last_update: datetime.datetime
