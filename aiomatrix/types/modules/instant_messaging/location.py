from typing import Optional

import pydantic

from .image import BasicImageInfo
from ..e2ee import EncryptedFile
from ...events.base import BasicRoomMessageEventContent
from ...misc import RoomMessageEventMsgTypesEnum


class LocationInfo(BasicImageInfo, pydantic.BaseModel):
    thumbnail_url: Optional[str]
    thumnail_file: Optional[EncryptedFile]
    thumbnail_info: Optional[BasicImageInfo]


class LocationContent(BasicRoomMessageEventContent):
    msgtype: RoomMessageEventMsgTypesEnum = RoomMessageEventMsgTypesEnum.location
    info: Optional[LocationInfo]
    geo_uri: str
