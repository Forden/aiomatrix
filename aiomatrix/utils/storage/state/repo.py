from typing import Dict, List

import aiomatrix
from . import BaseStateStorage, models


class StateRepo:
    def __init__(self, storage: BaseStateStorage):
        self.storage = storage

    async def get_event_data(self, event_id: str) -> models.StateEventInDB:
        return await self.storage.get_event_data(event_id)

    async def is_new_event(self, event_id: str) -> bool:
        return await self.storage.is_new_event(event_id)

    async def are_new_events(self, events_ids: List[str]) -> Dict[str, bool]:
        events_data = await self.storage.get_event_data_batch(events_ids)
        found_ids = set(map(lambda x: x.event_id, events_data))
        res = {i: i in found_ids for i in events_ids}
        return res

    async def insert_new_event(self, event: aiomatrix.models.events.RoomStateEvent):
        return await self.storage.insert_new_event(event)

    async def insert_new_events_batch(self, events: List[aiomatrix.models.events.RoomStateEvent]):
        return await self.storage.insert_new_events_batch(events)

    async def get_events_by_room(self, room_id: str) -> List[models.StateEventInDB]:
        return await self.storage.get_events_by_room(room_id)

    async def get_event_data_batch(self, events_ids: List[str]) -> Dict[str, models.StateEventInDB]:
        return await self.storage.get_event_data_batch(events_ids)
