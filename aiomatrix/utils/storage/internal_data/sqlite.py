import pathlib
from typing import Optional, Union

from . import BaseInternalDataStorage, engines, models


class SqliteInternalDataStorage(BaseInternalDataStorage):
    def __init__(self, db_path: Union[pathlib.Path, str]):
        self.db_mngr = engines.SqliteInternalDataStorageEngine(db_path)

    async def get_last_sync_token(self) -> Optional[models.InternalDataPair]:
        db_res = await self.db_mngr.get_data_by_key('sync_token')
        return db_res

    async def set_last_sync_token(self, token: str):
        if await self.get_last_sync_token() is not None:
            await self.db_mngr.set_data_by_key('sync_token', token)
        else:
            await self.db_mngr.insert_data('sync_token', token)
