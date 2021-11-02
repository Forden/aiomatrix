import pathlib
from typing import Optional, Union

from . import BaseInternalDataStorage, engines, models


class SqliteInternalDataStorage(BaseInternalDataStorage):
    def __init__(self, db_path: Union[pathlib.Path, str]):
        self.db_mngr = engines.SqliteInternalDataStorageEngine(db_path)

    async def setup(self):
        await self.db_mngr.create_internal_data_table()

    async def get_last_sync_token(self, account_id: str) -> Optional[models.InternalDataPair]:
        db_res = await self.db_mngr.get_data_by_key(account_id, 'sync_token')
        return db_res

    async def set_last_sync_token(self, account_id: str, token: str):
        if await self.get_last_sync_token(account_id) is not None:
            await self.db_mngr.set_data_by_key(account_id, 'sync_token', token)
        else:
            await self.db_mngr.insert_data(account_id, 'sync_token', token)
