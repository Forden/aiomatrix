from __future__ import annotations

from typing import Optional

from .basic_file_info import BasicFileInfo
from ..e2ee import EncryptedFile
from ...base_room_events import BaseMessageEventContent


class BasicImageInfo(BasicFileInfo):
    h: int
    w: int


class FileInfo(BasicImageInfo):
    thumbnail_url: Optional[str]
    thumnail_file: Optional[EncryptedFile]
    thumbnail_info: Optional[BasicImageInfo]


class ImageContent(BaseMessageEventContent):
    info: Optional[FileInfo]
    url: Optional[str]
    file: Optional[EncryptedFile]
