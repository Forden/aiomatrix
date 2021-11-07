from __future__ import annotations

from typing import Optional

from .image import BasicImageInfo
from ..e2ee import EncryptedFile
from ...base_room_events import BaseMessageEventContent


class LocationInfo(BasicImageInfo):
    thumbnail_url: Optional[str]
    thumnail_file: Optional[EncryptedFile]
    thumbnail_info: Optional[BasicImageInfo]


class LocationContent(BaseMessageEventContent):
    info: Optional[LocationInfo]
    geo_uri: str
