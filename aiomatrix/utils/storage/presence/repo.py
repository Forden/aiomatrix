from typing import List, Optional, Union

import aiomatrix.types.modules.presence.presence
from . import BasePresenceStorage, models


# TODO: remove account_id from storage
class PresenceRepo:
    def __init__(self, storage: BasePresenceStorage):
        self.storage = storage

    async def get_user_data(
            self, account_id: Union[str, aiomatrix.types.responses.WhoAmIResponse],
            user_id: aiomatrix.types.primitives.UserID
    ) -> Optional[models.PresenceInDB]:
        if isinstance(account_id, aiomatrix.types.responses.WhoAmIResponse):
            account_id = account_id.user_id
        return await self.storage.get_user_data(account_id, user_id)

    async def is_new_user(
            self, account_id: Union[str, aiomatrix.types.responses.WhoAmIResponse],
            user_id: aiomatrix.types.primitives.UserID
    ) -> bool:
        if isinstance(account_id, aiomatrix.types.responses.WhoAmIResponse):
            account_id = account_id.user_id
        return await self.storage.is_new_user(account_id, user_id)

    async def add_new_presence_update(
            self, account_id: Union[str, aiomatrix.types.responses.WhoAmIResponse],
            event: aiomatrix.types.modules.presence.PresenceEvent
    ):
        if isinstance(account_id, aiomatrix.types.responses.WhoAmIResponse):
            account_id = account_id.user_id
        return await self.storage.add_new_presence_update(account_id, event)

    async def update_user_presence(
            self, account_id: Union[str, aiomatrix.types.responses.WhoAmIResponse],
            user_id: aiomatrix.types.primitives.UserID, event: aiomatrix.types.modules.presence.CurrentPresenceStatus
    ):
        if isinstance(account_id, aiomatrix.types.responses.WhoAmIResponse):
            account_id = account_id.user_id
        return await self.storage.update_user_presence(account_id, user_id, event)

    async def get_outdated_users_data(
            self, account_id: Union[str, aiomatrix.types.responses.WhoAmIResponse], timeout: int = 60
    ) -> List[models.PresenceInDB]:
        if isinstance(account_id, aiomatrix.types.responses.WhoAmIResponse):
            account_id = account_id.user_id
        return await self.storage.get_unupdated_users(account_id, timeout)
