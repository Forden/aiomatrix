import pathlib
from typing import Dict, List, Optional, Union

import aiomatrix
from . import BaseEventStorage, engines, models


class SqliteEventStorage(BaseEventStorage):
    def __init__(self, db_path: Union[pathlib.Path, str]):
        self.db_mngr = engines.SqliteEventStorageEngine(db_path)

    async def get_event_data(
            self, event_id: aiomatrix.types.primitives.EventID
    ) -> Optional[models.EventInDB]:
        db_res = await self.db_mngr.get_event(event_id)
        return db_res

    async def is_new_event(self, event: aiomatrix.types.events.RoomEvent) -> bool:
        event_in_db = await self.get_event_data(event.event_id)
        return event_in_db is None

    async def insert_new_event(self, event: aiomatrix.types.events.RoomEvent):
        await self.db_mngr.add_new_state_event(event)

    async def insert_new_events_batch(self, events: List[aiomatrix.types.events.RoomEvent]):
        await self.db_mngr.add_new_state_events_batch(events)

    async def get_events_by_room(
            self, room_id: aiomatrix.types.primitives.RoomID
    ) -> List[models.EventInDB]:
        db_res = await self.db_mngr.get_room_events(room_id)
        return db_res

    async def get_multiple_events_data(
            self, events_ids: List[aiomatrix.types.primitives.EventID]
    ) -> Dict[str, models.EventInDB]:
        db_res = await self.db_mngr.get_events_batch(events_ids)
        res = {i.event_id: i for i in db_res}
        return res

    async def get_account_seen_events(self, account_id: str) -> List[models.SeenEvent]:
        db_res = await self.db_mngr.get_account_seen_events(account_id)
        return db_res

    async def check_seen_events(
            self, account_id: str, event_ids: List[aiomatrix.types.primitives.EventID]
    ) -> List[models.SeenEvent]:
        db_res = await self.db_mngr.check_seen_events(account_id, event_ids)
        return db_res

    async def add_new_seen_event(self, account_id: str, event_id: aiomatrix.types.primitives.EventID):
        await self.db_mngr.add_new_seen_event(account_id, event_id)

    async def add_new_seen_events_batch(self, account_id: str, event_ids: List[aiomatrix.types.primitives.EventID]):
        await self.db_mngr.add_new_seen_events_batch(account_id, event_ids)
