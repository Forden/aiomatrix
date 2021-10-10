import pathlib
from typing import List, Optional, Union

import aiomatrix
from . import BasePresenceStorage, engines, models


class SqlitePresenceStorage(BasePresenceStorage):
    def __init__(self, db_path: Union[pathlib.Path, str]):
        self.db_mngr = engines.SqlitePresenceStorageEngine(db_path)

    async def get_user_data(
            self, account_id: str, user_id: aiomatrix.types.primitives.UserID
    ) -> Optional[models.PresenceInDB]:
        db_res = await self.db_mngr.get_user_data(account_id, user_id)
        return db_res

    async def is_new_user(self, account_id: str, user_id: aiomatrix.types.primitives.UserID) -> bool:
        event_in_db = await self.get_user_data(account_id, user_id)
        return event_in_db is None

    async def add_new_presence_update(self, account_id: str, event: aiomatrix.types.modules.presence.PresenceEvent):
        if await self.is_new_user(account_id, event.sender):
            await self.db_mngr.add_new_presence(
                account_id, event.sender, event.content.presence, event.content.last_active_ago,
                event.content.status_msg
            )

    async def update_user_presence(
            self, account_id: str, user_id: aiomatrix.types.primitives.UserID,
            event: aiomatrix.types.modules.presence.CurrentPresenceStatus
    ):
        await self.db_mngr.update_user_presence(
            account_id, user_id, event.presence, event.last_active_ago, event.status_msg
        )

    async def get_unupdated_users(self, account_id: str, timeout: int) -> List[models.PresenceInDB]:
        db_res = await self.db_mngr.get_unupdated_users(account_id, timeout)
        return db_res
