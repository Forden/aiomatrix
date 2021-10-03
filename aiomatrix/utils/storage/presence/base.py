from typing import List, Optional

import aiomatrix.models.events
from . import models


class BasePresenceStorage:
    async def get_user_data(self, user_id: str) -> Optional[models.PresenceInDB]:
        raise NotImplementedError

    async def is_new_user(self, user_id: str) -> bool:
        raise NotImplementedError

    async def add_new_presence_update(self, event: aiomatrix.models.modules.presence.PresenceEvent):
        raise NotImplementedError

    async def update_user_presence(self, user_id: str, event: aiomatrix.models.modules.presence.CurrentPresenceStatus):
        raise NotImplementedError

    async def get_unupdated_users(self, timeout: int) -> List[models.PresenceInDB]:
        raise NotImplementedError
