from typing import List, Optional

import aiomatrix.types.events
from . import models


class BasePresenceStorage:
    async def get_user_data(self, user_id: aiomatrix.types.primitives.UserID) -> Optional[models.PresenceInDB]:
        raise NotImplementedError

    async def is_new_user(self, user_id: aiomatrix.types.primitives.UserID) -> bool:
        raise NotImplementedError

    async def add_new_presence_update(self, event: aiomatrix.types.modules.presence.PresenceEvent):
        raise NotImplementedError

    async def update_user_presence(
            self, user_id: aiomatrix.types.primitives.UserID,
            event: aiomatrix.types.modules.presence.CurrentPresenceStatus
    ):
        raise NotImplementedError

    async def get_unupdated_users(self, timeout: int) -> List[models.PresenceInDB]:
        raise NotImplementedError
