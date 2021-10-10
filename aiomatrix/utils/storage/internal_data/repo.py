from typing import Optional, Union

import aiomatrix.types.responses
from . import BaseInternalDataStorage


class InternalDataRepo:
    def __init__(self, storage: BaseInternalDataStorage):
        self.storage = storage

    async def get_last_sync_token(
            self, account_id: Union[str, aiomatrix.types.responses.WhoAmIResponse]
    ) -> Optional[str]:
        if isinstance(account_id, aiomatrix.types.responses.WhoAmIResponse):
            account_id = account_id.user_id
        db_res = await self.storage.get_last_sync_token(account_id)
        if db_res:
            return db_res.data
        return None

    async def set_last_sync_token(self, account_id: Union[str, aiomatrix.types.responses.WhoAmIResponse], token: str):
        if isinstance(account_id, aiomatrix.types.responses.WhoAmIResponse):
            account_id = account_id.user_id
        return await self.storage.set_last_sync_token(account_id, token)
