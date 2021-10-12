import typing
from typing import List, Union

from aiomatrix import types
from .base import BaseFilter

if typing.TYPE_CHECKING:
    from aiomatrix import AiomatrixClient


class RoomID(BaseFilter):
    def __init__(self, room_ids: List[str]):
        super().__init__()
        self.filter_id: str = 'room_id'
        self.room_ids = set(room_ids)

    async def check(self, event: types.events.RoomEvent, client: 'AiomatrixClient'):
        return event.room_id in self.room_ids


class EventType(BaseFilter):
    def __init__(self, event_types: List[Union[str, types.misc.RoomEventTypesEnum]]):
        super().__init__()
        self.filter_id: str = 'event_type'
        self.event_types = set(map(lambda x: f'{x}', event_types))

    async def check(self, event: types.events.RoomEvent, client: 'AiomatrixClient'):
        return event.type in self.event_types


class MessageType(BaseFilter):
    def __init__(self, msg_type: List[Union[str, types.misc.RoomMessageEventMsgTypesEnum]]):
        super().__init__()
        self.filter_id: str = 'message_type'
        self.message_types = set(map(lambda x: f'{x}', msg_type))

    async def check(self, event: types.events.RoomMessageEvent, client: 'AiomatrixClient'):
        try:
            if event.content is not None:
                return event.content.msgtype in self.message_types
        except AttributeError:
            return False


class SenderID(BaseFilter):
    def __init__(self, sender_ids: List[str]):
        super().__init__()
        self.filter_id: str = 'sender_id'
        self.sender_ids = set(sender_ids)

    async def check(self, event: types.events.RoomEvent, client: 'AiomatrixClient'):
        return event.sender in self.sender_ids


class Incoming(BaseFilter):
    """
    only incoming events
    """

    def __init__(self):
        super().__init__()
        self.filter_id: str = 'message_direction'

    async def check(self, event: types.events.RoomEvent, client: 'AiomatrixClient'):
        return event.sender != client.me.user_id


class Outgoing(BaseFilter):
    """
    only outgoing events
    """

    def __init__(self):
        super().__init__()
        self.filter_id: str = 'message_direction'

    async def check(self, event: types.events.RoomEvent, client: 'AiomatrixClient'):
        return event.sender == client.me.user_id


class Text(BaseFilter):
    def __init__(self, texts: List[str], case_insensitive: bool = True):
        super().__init__()
        self.filter_id: str = 'text'
        self.case_insensitive = case_insensitive
        if self.case_insensitive:
            self.allowed_texts = map(lambda x: x.lower(), texts)
        else:
            self.allowed_texts = texts
        self.allowed_texts = set(self.allowed_texts)

    async def check(self, event: types.events.RoomMessageEvent, client: 'AiomatrixClient'):
        event_txt = event.content.body
        if self.case_insensitive:
            event_txt = event_txt.lower()
        return event_txt in self.allowed_texts


class Command(Text):
    def __init__(self, commands: List[str], prefix: str = '!'):
        super().__init__(list(map(lambda x: f'{prefix}{x}', commands)), True)
