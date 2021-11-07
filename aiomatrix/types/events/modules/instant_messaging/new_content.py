from __future__ import annotations

import typing

from pydantic import Field, validator

from aiomatrix.types.misc import RoomMessageEventMsgTypesEnum
from ...base_room_events import BaseMessageEventContent

if typing.TYPE_CHECKING:
    from .audio import AudioContent
    from .emote import EmoteContent
    from .file import FileContent
    from .image import ImageContent
    from .location import LocationContent
    from .notice import NoticeContent
    from .video import VideoContent
    from .text import TextContent


class NewContent(BaseMessageEventContent):
    new_content: typing.Union[
        AudioContent, EmoteContent, FileContent, ImageContent, LocationContent, NoticeContent, TextContent, VideoContent
    ] = Field(..., alias='m.new_content')

    @validator('new_content')
    def _fix_typing(cls, v: typing.Union[
        AudioContent, EmoteContent, FileContent, ImageContent, LocationContent, NoticeContent, TextContent, VideoContent
    ]):
        from .audio import AudioContent
        from .emote import EmoteContent
        from .file import FileContent
        from .image import ImageContent
        from .location import LocationContent
        from .notice import NoticeContent
        from .video import VideoContent
        from .text import TextContent
        supported_msgtypes = {
            RoomMessageEventMsgTypesEnum.audio:    AudioContent,
            RoomMessageEventMsgTypesEnum.emote:    EmoteContent,
            RoomMessageEventMsgTypesEnum.file:     FileContent,
            RoomMessageEventMsgTypesEnum.image:    ImageContent,
            RoomMessageEventMsgTypesEnum.location: LocationContent,
            RoomMessageEventMsgTypesEnum.notice:   NoticeContent,
            RoomMessageEventMsgTypesEnum.text:     TextContent,
            RoomMessageEventMsgTypesEnum.video:    VideoContent,
        }
        content = supported_msgtypes[v.msgtype](**v.raw)
        return content
