from typing import Optional

from pydantic import BaseModel

from .basic_file_info import BasicFileInfo
from .image import BasicImageInfo
from ..e2ee import EncryptedFile
from ...events import BasicRoomMessageEventContent


class FileInfo(BasicFileInfo, BaseModel):
    thumbnail_url: Optional[str]
    thumnail_file: Optional[EncryptedFile]
    thumbnail_info: Optional[BasicImageInfo]


class FileContent(BasicRoomMessageEventContent):
    info: Optional[FileInfo]
    url: Optional[str]
    file: Optional[EncryptedFile]
