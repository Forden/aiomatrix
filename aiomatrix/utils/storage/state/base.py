from typing import Dict, List, Optional

from aiomatrix import types
from . import models


class BaseStateStorage:
    async def get_event_data(self, event_id: types.primitives.EventID) -> Optional[models.StateEventInDB]:
        raise NotImplementedError

    async def is_new_event(self, event_id: types.primitives.EventID) -> bool:
        raise NotImplementedError

    async def get_events_by_room(self, room_id: types.primitives.RoomID) -> List[models.StateEventInDB]:
        raise NotImplementedError

    async def get_event_data_batch(self, event_ids: List[types.primitives.EventID]) -> Dict[str, models.StateEventInDB]:
        raise NotImplementedError

    async def insert_new_event(self, event: types.events.RoomStateEvent):
        raise NotImplementedError

    async def insert_new_events_batch(self, events: List[types.events.RoomStateEvent]):
        raise NotImplementedError
