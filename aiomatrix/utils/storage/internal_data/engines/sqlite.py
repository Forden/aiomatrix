from typing import List, Optional

from .. import models
from ...base_engines import SqliteConnection


class SqliteInternalDataStorageEngine(SqliteConnection):
    async def get_data_by_key(self, key: str) -> Optional[models.InternalDataPair]:
        sql = 'SELECT * FROM internal_data WHERE key = ?'
        params = (key,)
        return self._make_request(sql, params, fetch=True, model_type=models.InternalDataPair)

    async def get_all_data(self) -> List[models.InternalDataPair]:
        sql = 'SELECT * FROM internal_data WHERE key = ?'
        return self._make_request(sql, params=None, fetch=True, mult=True, model_type=models.InternalDataPair)

    async def insert_data(self, key: str, value: str):
        sql = 'INSERT INTO internal_data (key, data) VALUES (?, ?)'
        params = (key, f'{value}')
        self._make_request(sql, params)

    async def set_data_by_key(self, key: str, value: str):
        sql = 'UPDATE internal_data SET data = ? WHERE key = ?'
        params = (f'{value}', key)
        self._make_request(sql, params)

    async def delete_data_by_key(self, key: str):
        sql = 'DELETE FROM internal_data WHERE key = ?'
        params = (key,)
        self._make_request(sql, params)
