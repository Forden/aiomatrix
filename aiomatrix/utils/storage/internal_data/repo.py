from typing import Optional

from . import BaseInternalDataStorage


class InternalDataRepo:
    def __init__(self, storage: BaseInternalDataStorage):
        self.storage = storage

    async def get_last_sync_token(self) -> Optional[str]:
        db_res = await self.storage.get_last_sync_token()
        if db_res:
            return db_res.data
        return None

    async def set_last_sync_token(self, token: str):
        return await self.storage.set_last_sync_token(token)
