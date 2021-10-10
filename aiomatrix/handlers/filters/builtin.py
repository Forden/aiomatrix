from typing import List, Union

from aiomatrix import types
from .base import BaseFilter


class RoomId(BaseFilter):
    def __init__(self, room_ids: List[str]):
        self.room_ids = set(room_ids)

    async def check(self, event: types.events.RoomEvent):
        return event.room_id in self.room_ids


class EventType(BaseFilter):
    def __init__(
            self,
            event_types: List[Union[str, types.misc.RoomEventTypesEnum]],
    ):
        self.event_types = set(map(lambda x: f'{x}', event_types))

    async def check(self, event: types.events.RoomEvent):
        return event.type in self.event_types


class MessageType(BaseFilter):
    def __init__(
            self,
            msg_type: List[Union[str, types.misc.RoomMessageEventMsgTypesEnum]]
    ):
        self.message_types = set(map(lambda x: f'{x}', msg_type))

    async def check(self, event: types.events.RoomMessageEvent):
        if event.content is not None:
            return event.content.msgtype in self.message_types
