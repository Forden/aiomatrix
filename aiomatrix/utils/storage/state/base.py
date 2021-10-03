from typing import Dict, List, Optional, Set, Union

import aiomatrix.models.events
from . import models


class BaseStateStorage:
    async def get_event_data(self, event_id: str) -> Optional[models.EventInDB]:
        raise NotImplementedError

    async def is_new_event(self, event_id: str) -> bool:
        raise NotImplementedError

    async def get_events_by_room(self, room_id: str) -> List[models.EventInDB]:
        raise NotImplementedError

    async def get_event_data_batch(
            self, event_ids: List[str], only_ids: bool
    ) -> Union[Dict[str, models.EventInDB], Set[str]]:
        raise NotImplementedError

    async def insert_new_event(self, event: aiomatrix.models.events.RoomStateEvent):
        raise NotImplementedError

    async def insert_new_events_batch(self, events: List[aiomatrix.models.events.RoomStateEvent]):
        raise NotImplementedError
