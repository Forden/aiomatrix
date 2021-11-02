from typing import Dict, List, Optional

from aiomatrix import types
from . import models


class BaseEventStorage:
    async def setup(self):
        raise NotImplementedError
    
    async def get_event_data(
            self, event_id: types.primitives.EventID
    ) -> Optional[models.EventInDB]:
        raise NotImplementedError

    async def is_new_event(self, event_id: types.primitives.EventID) -> bool:
        raise NotImplementedError

    async def get_events_by_room(
            self, room_id: types.primitives.RoomID
    ) -> List[models.EventInDB]:
        raise NotImplementedError

    async def get_multiple_events_data(
            self, event_ids: List[types.primitives.EventID]
    ) -> Dict[str, models.EventInDB]:
        raise NotImplementedError

    async def insert_new_event(self, event: types.events.RoomEvent):
        raise NotImplementedError

    async def insert_new_events_batch(self, events: List[types.events.RoomEvent]):
        raise NotImplementedError

    async def get_account_seen_events(self, account_id: str) -> List[models.SeenEvent]:
        raise NotImplementedError

    async def check_seen_events(
            self, account_id: str, event_ids: List[types.primitives.EventID]
    ) -> List[models.SeenEvent]:
        raise NotImplementedError

    async def add_new_seen_event(self, account_id: str, event_id: types.primitives.EventID):
        raise NotImplementedError

    async def add_new_seen_events_batch(self, account_id: str, event_ids: List[types.primitives.EventID]):
        raise NotImplementedError
