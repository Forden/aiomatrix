from __future__ import annotations

from typing import Optional

from .basic_file_info import BasicFileInfo
from .image import BasicImageInfo
from ..e2ee import EncryptedFile
from ...base_room_events import BaseMessageEventContent


class VideoInfo(BasicFileInfo):
    duration: str
    h: int
    w: int
    thumbnail_url: Optional[str]
    thumnail_file: Optional[EncryptedFile]
    thumbnail_info: Optional[BasicImageInfo]


class VideoContent(BaseMessageEventContent):
    info: Optional[VideoInfo]
    url: Optional[str]
    file: Optional[EncryptedFile]
