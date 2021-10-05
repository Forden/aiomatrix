from typing import Optional

import pydantic

from .basic_file_info import BasicFileInfo
from ..e2ee import EncryptedFile
from ...events.base import BasicRoomMessageEventContent
from ...misc import RoomMessageEventMsgTypesEnum


class BasicImageInfo(BasicFileInfo):
    h: int
    w: int


class FileInfo(BasicImageInfo, pydantic.BaseModel):
    thumbnail_url: Optional[str]
    thumnail_file: Optional[EncryptedFile]
    thumbnail_info: Optional[BasicImageInfo]


class ImageContent(BasicRoomMessageEventContent):
    msgtype: RoomMessageEventMsgTypesEnum = RoomMessageEventMsgTypesEnum.image
    info: Optional[FileInfo]
    formatted_body: Optional[str]
    url: Optional[str]
    file: Optional[EncryptedFile]
