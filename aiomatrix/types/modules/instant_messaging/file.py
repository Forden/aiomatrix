from typing import Optional

import pydantic

from .basic_file_info import BasicFileInfo
from .image import BasicImageInfo
from ..e2ee import EncryptedFile
from ...events.base import BasicRoomMessageEventContent
from ...misc import RoomMessageEventMsgTypesEnum


class FileInfo(BasicFileInfo, pydantic.BaseModel):
    thumbnail_url: Optional[str]
    thumnail_file: Optional[EncryptedFile]
    thumbnail_info: Optional[BasicImageInfo]


class FileContent(BasicRoomMessageEventContent):
    msgtype: RoomMessageEventMsgTypesEnum = RoomMessageEventMsgTypesEnum.file
    info: Optional[FileInfo]
    url: Optional[str]
    file: Optional[EncryptedFile]
