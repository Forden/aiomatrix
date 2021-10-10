from typing import Dict, List, Optional, Union

import aiomatrix
from . import BaseStateStorage, models


class StateRepo:
    def __init__(self, storage: BaseStateStorage):
        self.storage = storage

    async def get_event_data(
            self, account_id: Union[str, aiomatrix.types.responses.WhoAmIResponse],
            event_id: aiomatrix.types.primitives.EventID
    ) -> Optional[models.EventInDB]:
        if isinstance(account_id, aiomatrix.types.responses.WhoAmIResponse):
            account_id = account_id.user_id
        is_seen_event = event_id in (await self.storage.check_seen_events(account_id, [event_id]))
        if is_seen_event:
            return await self.storage.get_event_data(event_id)
        else:
            return None

    async def get_event_data_batch(
            self, account_id: Union[str, aiomatrix.types.responses.WhoAmIResponse],
            events_ids: List[aiomatrix.types.primitives.EventID]
    ) -> Dict[str, models.EventInDB]:
        if isinstance(account_id, aiomatrix.types.responses.WhoAmIResponse):
            account_id = account_id.user_id
        seen_events = list(map(lambda x: x.event_id, await self.storage.check_seen_events(account_id, events_ids)))
        return await self.storage.get_multiple_events_data(seen_events)

    async def is_new_event(
            self, account_id: Union[str, aiomatrix.types.responses.WhoAmIResponse],
            event_id: aiomatrix.types.primitives.EventID
    ) -> bool:
        if isinstance(account_id, aiomatrix.types.responses.WhoAmIResponse):
            account_id = account_id.user_id
        is_seen_event = event_id in (await self.storage.check_seen_events(account_id, [event_id]))
        if is_seen_event:
            return await self.storage.is_new_event(event_id)
        else:
            return True

    async def are_new_events(
            self, account_id: Union[str, aiomatrix.types.responses.WhoAmIResponse],
            events_ids: List[aiomatrix.types.primitives.EventID]
    ) -> Dict[str, bool]:
        if isinstance(account_id, aiomatrix.types.responses.WhoAmIResponse):
            account_id = account_id.user_id
        events_data = await self.storage.check_seen_events(account_id, events_ids)
        found_ids = set(map(lambda x: x.event_id, events_data))
        res = {i: i in found_ids for i in events_ids}
        return res

    async def insert_new_event(
            self, account_id: Union[str, aiomatrix.types.responses.WhoAmIResponse],
            event: aiomatrix.types.events.RoomEvent
    ):
        if isinstance(account_id, aiomatrix.types.responses.WhoAmIResponse):
            account_id = account_id.user_id
        await self.storage.add_new_seen_event(account_id, event.event_id)
        return await self.storage.insert_new_event(event)

    async def insert_new_events_batch(
            self, account_id: Union[str, aiomatrix.types.responses.WhoAmIResponse],
            events: List[aiomatrix.types.events.RoomEvent]
    ):
        if isinstance(account_id, aiomatrix.types.responses.WhoAmIResponse):
            account_id = account_id.user_id
        await self.storage.add_new_seen_events_batch(account_id, list(map(lambda x: x.event_id, events)))
        return await self.storage.insert_new_events_batch(events)

    # TODO: implement with account_id in mind
    # async def get_events_by_room(
    #         self, account_id: Union[str, aiomatrix.types.responses.WhoAmIResponse],
    #         room_id: aiomatrix.types.primitives.RoomID
    # ) -> List[models.EventInDB]:
    #     if isinstance(account_id, aiomatrix.types.responses.WhoAmIResponse):
    #         account_id = account_id.user_id
    #     return await self.storage.get_events_by_room(account_id, room_id)
