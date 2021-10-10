from typing import List, Optional

import aiomatrix
from .. import models
from ...base_engines import SqliteConnection


class SqliteStateStorageEngine(SqliteConnection):
    async def get_event(self, event_id: aiomatrix.types.primitives.EventID) -> Optional[models.EventInDB]:
        sql = 'SELECT * FROM events WHERE event_id = ?'
        params = (event_id,)
        r = self._make_request(sql, params, fetch=True, model_type=models.EventInDB)
        return r

    async def get_events_batch(
            self, events_ids: List[aiomatrix.types.primitives.EventID]
    ) -> List[models.EventInDB]:
        # noinspection SqlResolve
        sql = f'SELECT * FROM events WHERE event_id IN ({", ".join(["?" for _ in range(len(events_ids))])})'
        params = tuple([*events_ids])
        r = self._make_request(sql, params, fetch=True, mult=True, model_type=models.EventInDB)
        return r

    async def add_new_state_event(self, event: aiomatrix.types.events.RoomEvent):
        sql = 'INSERT INTO events (event_id, room_id, sender, ts, event_type, data) VALUES (?, ?, ?, ?, ?, ?)'
        params = (
            event.event_id, event.room_id, event.sender, int(event.timestamp.timestamp()), event.type,
            event.json(by_alias=True)
        )
        self._make_request(sql, params)

    async def add_new_state_events_batch(self, events: List[aiomatrix.types.events.RoomEvent]):
        sql = 'INSERT INTO events (event_id, room_id, sender, ts, event_type, data) VALUES (?, ?, ?, ?, ?, ?)'
        params = [
            (
                event.event_id, event.room_id, event.sender, int(event.timestamp.timestamp()), event.type,
                event.json(by_alias=True)
            )
            for event in events
        ]
        self._make_request(sql, params)

    async def get_room_events(
            self, room_id: aiomatrix.types.primitives.RoomID
    ) -> List[models.EventInDB]:
        sql = 'SELECT * FROM events WHERE room_id = ? ORDER BY ts'
        params = (room_id,)
        r = self._make_request(sql, params, fetch=True, mult=True, model_type=models.EventInDB)
        return r

    async def get_account_seen_events(self, account_id: str) -> List[models.SeenEvent]:
        sql = 'SELECT * FROM seen_events WHERE account_id = ?'
        params = (account_id,)
        r = self._make_request(sql, params, fetch=True, mult=True, model_type=models.SeenEvent)
        return r

    async def check_seen_events(
            self, account_id: str, events_ids: List[aiomatrix.types.primitives.EventID]
    ) -> List[models.SeenEvent]:
        # noinspection SqlResolve
        sql = f'SELECT * FROM seen_events WHERE account_id = ? AND event_id IN ({", ".join(["?" for _ in range(len(events_ids))])})'
        params = tuple([account_id, *events_ids])
        r = self._make_request(sql, params, fetch=True, mult=True, model_type=models.SeenEvent)
        return r

    async def add_new_seen_event(self, account_id: str, event_id: aiomatrix.types.primitives.EventID):
        sql = 'INSERT INTO seen_events (account_id, event_ID) VALUES (?, ?)'
        params = (account_id, event_id)
        self._make_request(sql, params)

    async def add_new_seen_events_batch(self, account_id: str, event_ids: List[aiomatrix.types.primitives.EventID]):
        sql = 'INSERT INTO seen_events (account_id, event_ID) VALUES (?, ?)'
        params = [(account_id, event_id) for event_id in event_ids]
        self._make_request(sql, params)
