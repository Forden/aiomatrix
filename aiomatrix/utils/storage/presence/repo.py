from typing import List, Optional

import aiomatrix.types.modules.presence.presence
from . import BasePresenceStorage, models


class PresenceRepo:
    def __init__(self, storage: BasePresenceStorage):
        self.storage = storage

    async def get_user_data(self, user_id: aiomatrix.types.primitives.UserID) -> Optional[models.PresenceInDB]:
        return await self.storage.get_user_data(user_id)

    async def is_new_user(self, user_id: aiomatrix.types.primitives.UserID) -> bool:
        return await self.storage.is_new_user(user_id)

    async def add_new_presence_update(self, event: aiomatrix.types.modules.presence.PresenceEvent):
        return await self.storage.add_new_presence_update(event)

    async def update_user_presence(
            self, user_id: aiomatrix.types.primitives.UserID,
            event: aiomatrix.types.modules.presence.CurrentPresenceStatus
    ):
        return await self.storage.update_user_presence(user_id, event)

    async def get_outdated_users_data(self, timeout: int = 60) -> List[models.PresenceInDB]:
        return await self.storage.get_unupdated_users(timeout)
