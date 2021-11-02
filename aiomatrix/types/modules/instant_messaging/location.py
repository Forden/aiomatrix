from typing import Optional

from pydantic import BaseModel

from .image import BasicImageInfo
from ..e2ee import EncryptedFile
from ...events import BasicRoomMessageEventContent


class LocationInfo(BasicImageInfo, BaseModel):
    thumbnail_url: Optional[str]
    thumnail_file: Optional[EncryptedFile]
    thumbnail_info: Optional[BasicImageInfo]


class LocationContent(BasicRoomMessageEventContent):
    info: Optional[LocationInfo]
    geo_uri: str
