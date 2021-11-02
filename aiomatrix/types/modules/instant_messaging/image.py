from typing import Optional

from pydantic import BaseModel

from .basic_file_info import BasicFileInfo
from ..e2ee import EncryptedFile
from ...events import BasicRoomMessageEventContent


class BasicImageInfo(BasicFileInfo):
    h: int
    w: int


class FileInfo(BasicImageInfo, BaseModel):
    thumbnail_url: Optional[str]
    thumnail_file: Optional[EncryptedFile]
    thumbnail_info: Optional[BasicImageInfo]


class ImageContent(BasicRoomMessageEventContent):
    info: Optional[FileInfo]
    formatted_body: Optional[str]
    url: Optional[str]
    file: Optional[EncryptedFile]
