from typing import Optional

from pydantic import BaseModel

from .basic_file_info import BasicFileInfo
from .image import BasicImageInfo
from ..e2ee import EncryptedFile
from ...events.base import BasicRoomMessageEventContent


class VideoInfo(BasicFileInfo, BaseModel):
    duration: str
    h: int
    w: int
    thumbnail_url: Optional[str]
    thumnail_file: Optional[EncryptedFile]
    thumbnail_info: Optional[BasicImageInfo]


class VideoContent(BasicRoomMessageEventContent):
    info: Optional[VideoInfo]
    url: Optional[str]
    file: Optional[EncryptedFile]
