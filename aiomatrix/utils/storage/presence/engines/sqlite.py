import datetime
from typing import List, Optional

import aiomatrix
from .. import models
from ...base_engines import SqliteConnection


class SqlitePresenceStorageEngine(SqliteConnection):
    async def create_presence_table(self):
        sql = '''
            create table if not exists presence
            (
                account_id  TEXT,
                user_id     TEXT,
                presence    TEXT,
                last_active INTEGER,
                status_msg  TEXT,
                last_update INTEGER,
                UNIQUE (account_id, user_id) ON CONFLICT IGNORE,
                PRIMARY KEY (account_id, user_id)
            );
        '''
        self._make_request(sql)

    async def get_user_data(
            self, account_id: str, user_id: aiomatrix.types.primitives.UserID
    ) -> Optional[models.PresenceInDB]:
        sql = 'SELECT * FROM presence WHERE user_id = ? AND account_id = ?'
        params = (user_id, account_id)
        r = self._make_request(sql, params, fetch=True, model_type=models.PresenceInDB)
        return r

    async def add_new_presence(
            self, account_id: str, user_id: aiomatrix.types.primitives.UserID,
            presence: aiomatrix.types.misc.PresenceEnum, last_active_ago: Optional[int] = None,
            status_msg: Optional[str] = None
    ):
        now = datetime.datetime.utcnow()
        sql = 'INSERT INTO presence (user_id, presence, last_active, status_msg, last_update, account_id) VALUES (?, ?, ?, ?, ?, ?)'
        params = (
            user_id, f'{presence}',
            datetime.datetime.fromtimestamp(now.timestamp() - last_active_ago).isoformat() if last_active_ago else None,
            status_msg, now.isoformat(), account_id
        )
        self._make_request(sql, params)

    async def update_user_presence(
            self, account_id: str, user_id: aiomatrix.types.primitives.UserID,
            presence: aiomatrix.types.misc.PresenceEnum,
            last_active_ago: Optional[int] = None, status_msg: Optional[str] = None
    ):
        now = datetime.datetime.utcnow()
        sql = 'UPDATE presence SET presence = ?, last_active = ?, status_msg = ?, last_update = ? WHERE user_id = ? AND account_id = ?'
        params = (
            f'{presence}',
            datetime.datetime.fromtimestamp(now.timestamp() - last_active_ago).isoformat() if last_active_ago else None,
            status_msg, now.isoformat(), user_id, account_id
        )
        self._make_request(sql, params)

    async def get_unupdated_users(self, account_id: str, timeout: int) -> List[models.PresenceInDB]:
        sql = 'SELECT * FROM presence WHERE last_active + ? < ? AND account_id = ?'
        params = (timeout, datetime.datetime.utcnow().timestamp() + timeout, account_id)
        r = self._make_request(sql, params, fetch=True, mult=True, model_type=models.PresenceInDB)
        return r
