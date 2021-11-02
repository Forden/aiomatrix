from typing import List, Optional

from .. import models
from ...base_engines import SqliteConnection


class SqliteInternalDataStorageEngine(SqliteConnection):
    async def create_internal_data_table(self):
        sql = '''
            create table if not exists internal_data
            (
                account_id TEXT,
                key        TEXT,
                data       TEXT,
                UNIQUE (account_id, key) ON CONFLICT ABORT,
                PRIMARY KEY (account_id, key)
            );
        '''
        self._make_request(sql)

    async def get_data_by_key(self, account_id: str, key: str) -> Optional[models.InternalDataPair]:
        sql = 'SELECT * FROM internal_data WHERE key = ? AND account_id = ?'
        params = (key, account_id)
        return self._make_request(sql, params, fetch=True, model_type=models.InternalDataPair)

    async def get_all_data(self, account_id: str) -> List[models.InternalDataPair]:
        sql = 'SELECT * FROM internal_data WHERE account_id = ?'
        params = (account_id,)
        return self._make_request(sql, params=params, fetch=True, mult=True, model_type=models.InternalDataPair)

    async def insert_data(self, account_id: str, key: str, value: str):
        sql = 'INSERT INTO internal_data (key, data, account_id) VALUES (?, ?, ?)'
        params = (key, f'{value}', account_id)
        self._make_request(sql, params)

    async def set_data_by_key(self, account_id: str, key: str, value: str):
        sql = 'UPDATE internal_data SET data = ? WHERE key = ?AND account_id = ?'
        params = (f'{value}', key, account_id)
        self._make_request(sql, params)

    async def delete_data_by_key(self, account_id: str, key: str):
        sql = 'DELETE FROM internal_data WHERE key = ? AND account_id = ?'
        params = (key, account_id)
        self._make_request(sql, params)
