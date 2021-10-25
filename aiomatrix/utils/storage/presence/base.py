from typing import List, Optional

import aiomatrix.types.events
from . import models


class BasePresenceStorage:
    async def setup(self):
        raise NotImplementedError

    async def get_user_data(
            self, account_id: str, user_id: aiomatrix.types.primitives.UserID
    ) -> Optional[models.PresenceInDB]:
        raise NotImplementedError

    async def is_new_user(self, account_id: str, user_id: aiomatrix.types.primitives.UserID) -> bool:
        raise NotImplementedError

    async def add_new_presence_update(self, account_id: str, event: aiomatrix.types.modules.presence.PresenceEvent):
        raise NotImplementedError

    async def update_user_presence(
            self, account_id: str, user_id: aiomatrix.types.primitives.UserID,
            event: aiomatrix.types.modules.presence.CurrentPresenceStatus
    ):
        raise NotImplementedError

    async def get_unupdated_users(self, account_id: str, timeout: int) -> List[models.PresenceInDB]:
        raise NotImplementedError
