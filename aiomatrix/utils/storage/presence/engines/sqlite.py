import datetime
from typing import List, Optional

import aiomatrix
from .. import models
from ...base_engines import SqliteConnection


class SqlitePresenceStorageEngine(SqliteConnection):
    async def get_user_data(self, user_id: aiomatrix.types.primitives.UserID) -> Optional[models.PresenceInDB]:
        sql = 'SELECT * FROM presence WHERE user_id = ?'
        params = (user_id,)
        r = self._make_request(sql, params, fetch=True, model_type=models.PresenceInDB)
        return r

    async def add_new_presence(
            self, user_id: aiomatrix.types.primitives.UserID, presence: aiomatrix.types.misc.PresenceEnum,
            last_active_ago: Optional[int] = None, status_msg: Optional[str] = None
    ):
        now = datetime.datetime.utcnow()
        sql = 'INSERT INTO presence (user_id, presence, last_active, status_msg, last_update) VALUES (?, ?, ?, ?, ?)'
        params = (
            user_id, f'{presence}',
            datetime.datetime.fromtimestamp(now.timestamp() - last_active_ago).isoformat() if last_active_ago else None,
            status_msg, now.isoformat()
        )
        self._make_request(sql, params)

    async def update_user_presence(
            self, user_id: aiomatrix.types.primitives.UserID, presence: aiomatrix.types.misc.PresenceEnum,
            last_active_ago: Optional[int] = None, status_msg: Optional[str] = None
    ):
        now = datetime.datetime.utcnow()
        sql = 'UPDATE presence SET presence = ?, last_active = ?, status_msg = ?, last_update = ? WHERE user_id = ?'
        params = (
            f'{presence}',
            datetime.datetime.fromtimestamp(now.timestamp() - last_active_ago).isoformat() if last_active_ago else None,
            status_msg, now.isoformat(), user_id
        )
        self._make_request(sql, params)

    async def get_unupdated_users(self, timeout: int) -> List[models.PresenceInDB]:
        sql = 'SELECT * FROM presence WHERE last_active + ? < ?'
        params = (timeout, datetime.datetime.utcnow().timestamp() + timeout)
        r = self._make_request(sql, params, fetch=True, mult=True, model_type=models.PresenceInDB)
        return r
