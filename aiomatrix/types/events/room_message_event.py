from __future__ import annotations

import typing

from pydantic import validator

from .base_room_events import RoomEvent
from .modules import instant_messaging
from ..misc import RoomMessageEventMsgTypesEnum

if typing.TYPE_CHECKING:
    from ..responses import SentEventResponse


class RoomMessageEvent(RoomEvent):
    content: typing.Optional[
        typing.Union[
            instant_messaging.NewContent, instant_messaging.LocationContent, instant_messaging.TextContent,
            instant_messaging.NoticeContent, instant_messaging.AudioContent, instant_messaging.EmoteContent,
            instant_messaging.FileContent, instant_messaging.ImageContent, instant_messaging.VideoContent,
        ]
    ]

    @validator('content')
    def _fix_typing(
            cls,
            v: typing.Optional[
                typing.Union[
                    instant_messaging.NewContent, instant_messaging.LocationContent, instant_messaging.TextContent,
                    instant_messaging.NoticeContent, instant_messaging.AudioContent, instant_messaging.EmoteContent,
                    instant_messaging.FileContent, instant_messaging.ImageContent, instant_messaging.VideoContent
                ]
            ]
    ):
        if v is not None:
            supported_msgtypes = {
                RoomMessageEventMsgTypesEnum.audio:    instant_messaging.AudioContent,
                RoomMessageEventMsgTypesEnum.emote:    instant_messaging.EmoteContent,
                RoomMessageEventMsgTypesEnum.file:     instant_messaging.FileContent,
                RoomMessageEventMsgTypesEnum.image:    instant_messaging.ImageContent,
                RoomMessageEventMsgTypesEnum.location: instant_messaging.LocationContent,
                RoomMessageEventMsgTypesEnum.notice:   instant_messaging.NoticeContent,
                RoomMessageEventMsgTypesEnum.text:     instant_messaging.TextContent,
                RoomMessageEventMsgTypesEnum.video:    instant_messaging.VideoContent,
            }
            raw_content = v.raw
            if 'm.new_content' in raw_content and isinstance(v.raw['m.new_content'], dict):
                if 'msgtype' not in raw_content['m.new_content']:
                    raise ValueError('not found message type in new content')
                if raw_content['m.new_content']['msgtype'] not in supported_msgtypes:
                    raise ValueError(f'unknown new content type: {raw_content["msgtype"]["m.new_content"]}')
                content = instant_messaging.NewContent.parse_obj(raw_content)
            else:
                if 'msgtype' not in raw_content:
                    return None
                if raw_content['msgtype'] not in supported_msgtypes:
                    raise ValueError(f'unknown message type: {raw_content["msgtype"]}')
                content = supported_msgtypes[raw_content['msgtype']](**raw_content)
            return content

    async def send_typing(self, timeout: int = 5000):
        await self.client.typing_notifications_api.send_typing(self.client.me.user_id, self.room_id, timeout)

    async def send_notice(self, text: str) -> 'SentEventResponse':
        return await self.client.instant_messaging_api.send_notice(self.room_id, text)

    async def answer_notice(self, text: str) -> 'SentEventResponse':
        return await self.client.instant_messaging_api.send_notice(self.room_id, text, reply_to=self.event_id)
