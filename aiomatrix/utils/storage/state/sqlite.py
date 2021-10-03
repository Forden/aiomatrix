import pathlib
from typing import Dict, List, Optional, Set, Union

import aiomatrix
from . import BaseStateStorage, engines, models


class SqliteStateStorage(BaseStateStorage):
    def __init__(self, db_path: Union[pathlib.Path, str]):
        self.db_mngr = engines.SqliteStateStorageEngine(db_path)

    async def get_event_data(self, event_id: str) -> Optional[models.EventInDB]:
        db_res = await self.db_mngr.get_event(event_id)
        return db_res

    async def is_new_event(self, event: aiomatrix.models.events.RoomStateEvent) -> bool:
        event_in_db = await self.get_event_data(event.event_id)
        return event_in_db is None

    async def insert_new_event(self, event: aiomatrix.models.events.RoomStateEvent):
        await self.db_mngr.add_new_state_event(event)

    async def insert_new_events_batch(self, events: List[aiomatrix.models.events.RoomStateEvent]):
        await self.db_mngr.add_new_state_events_batch(events)

    async def get_events_by_room(self, room_id: str) -> List[models.EventInDB]:
        db_res = await self.db_mngr.get_room_events(room_id)
        return db_res

    async def get_event_data_batch(
            self, events_ids: List[str], only_ids: bool = False
    ) -> Union[Dict[str, models.EventInDB], Set[str]]:
        db_res = await self.db_mngr.get_events_batch(events_ids)
        if only_ids:
            return {i.event_id for i in db_res}
        else:
            res = {i.event_id: i for i in db_res}
        return res
