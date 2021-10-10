from typing import Optional

import pydantic

from .image import BasicImageInfo
from ..e2ee import EncryptedFile
from ...events.base import BasicRoomMessageEventContent


class LocationInfo(BasicImageInfo, pydantic.BaseModel):
    thumbnail_url: Optional[str]
    thumnail_file: Optional[EncryptedFile]
    thumbnail_info: Optional[BasicImageInfo]


class LocationContent(BasicRoomMessageEventContent):
    info: Optional[LocationInfo]
    geo_uri: str
