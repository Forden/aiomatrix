import pathlib
from typing import List, Optional, Union

import aiomatrix
from . import engines, models


class PresenceStorage:
    def __init__(self, db_path: Union[pathlib.Path, str]):
        self.db_mngr = engines.sqlite.PresenceStorage(db_path)

    async def get_user_data(self, user_id: str) -> Optional[models.PresenceInDB]:
        db_res = await self.db_mngr.get_user_data(user_id)
        return db_res

    async def is_new_user(self, event: aiomatrix.models.modules.presence.PresenceEvent):
        event_in_db = await self.get_user_data(event.sender)
        return event_in_db is None

    async def add_new_presence_update(self, event: aiomatrix.models.modules.presence.PresenceEvent):
        if await self.is_new_user(event):
            await self.db_mngr.add_new_presence(
                event.sender, event.content.presence, event.content.last_active_ago, event.content.status_msg
            )

    async def update_user_presence(
            self, user_id: str, event: aiomatrix.models.modules.presence.CurrentPresenceStatus
    ):
        await self.db_mngr.update_user_presence(user_id, event.presence, event.last_active_ago, event.status_msg)

    async def get_unupdated_users(self, timeout: int = 60) -> List[models.PresenceInDB]:
        db_res = await self.db_mngr.get_unupdated_users(timeout)
        return db_res
