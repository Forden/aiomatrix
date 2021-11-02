import typing
from typing import Union

from pydantic import Field

from .base_room_events import RelationshipMixin, RoomEvent
from ..misc import RoomMessageEventMsgTypesEnum

if typing.TYPE_CHECKING:
    from ..responses import SentEventResponse


class BasicRoomMessageEventContent(RelationshipMixin):
    body: str
    msgtype: Union[RoomMessageEventMsgTypesEnum, str]
    new_content: 'BasicRoomMessageEventContent' = Field(None, alias='m.new_content')


class RoomMessageEvent(RoomEvent):
    content: BasicRoomMessageEventContent

    async def send_typing(self, timeout: int = 5000):
        await self.client.typing_notifications_api.send_typing(self.client.me.user_id, self.room_id, timeout)

    async def send_notice(self, text: str) -> 'SentEventResponse':
        return await self.client.instant_messaging_api.send_notice(self.room_id, text)

    async def answer_notice(self, text: str) -> 'SentEventResponse':
        return await self.client.instant_messaging_api.send_notice(self.room_id, text, reply_to=self.event_id)


BasicRoomMessageEventContent.update_forward_refs()
