from typing import List, Optional

import aiomatrix
from .. import models
from ...base_engines import SqliteConnection


class SqliteStateStorageEngine(SqliteConnection):
    async def get_event(self, event_id: aiomatrix.types.primitives.EventID) -> Optional[models.StateEventInDB]:
        sql = 'SELECT * FROM events WHERE event_id = ?'
        params = (event_id,)
        r = self._make_request(sql, params, fetch=True, model_type=models.StateEventInDB)
        return r

    async def get_events_batch(
            self, events_ids: List[aiomatrix.types.primitives.EventID]
    ) -> List[models.StateEventInDB]:
        # noinspection SqlResolve
        sql = f'SELECT * FROM events WHERE event_id IN ({", ".join(["?" for _ in range(len(events_ids))])})'
        params = tuple(events_ids)
        r = self._make_request(sql, params, fetch=True, mult=True, model_type=models.StateEventInDB)
        return r

    async def add_new_state_event(self, event: aiomatrix.types.events.RoomStateEvent):
        sql = 'INSERT INTO events (event_id, room_id, sender, ts, event_type, data) VALUES (?, ?, ?, ?, ?, ?)'
        params = (
            event.event_id, event.room_id, event.sender, int(event.timestamp.timestamp()), event.type,
            event.json()
        )
        self._make_request(sql, params)

    async def add_new_state_events_batch(self, events: List[aiomatrix.types.events.RoomStateEvent]):
        sql = 'INSERT INTO events (event_id, room_id, sender, ts, event_type, data) VALUES (?, ?, ?, ?, ?, ?)'
        params = [
            (
                event.event_id, event.room_id, event.sender, int(event.timestamp.timestamp()), event.type,
                event.json()
            )
            for event in events
        ]
        self._make_request(sql, params)

    async def get_room_events(self, room_id: aiomatrix.types.primitives.RoomID) -> List[models.StateEventInDB]:
        sql = 'SELECT * FROM events WHERE room_id = ? ORDER BY ts '
        params = (room_id,)
        r = self._make_request(sql, params, fetch=True, mult=True, model_type=models.StateEventInDB)
        return r
