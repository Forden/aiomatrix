from typing import Optional

import pydantic

from .basic_file_info import BasicFileInfo
from ..e2ee import EncryptedFile
from ...events.basic import BasicRoomMessageEventContent, RoomMessageEventMsgTypesEnum


class AudioInfo(BasicFileInfo, pydantic.BaseModel):
    duration: int


class Audio(BasicRoomMessageEventContent):
    msgtype: RoomMessageEventMsgTypesEnum = RoomMessageEventMsgTypesEnum.audio
    info: Optional[AudioInfo]
    url: Optional[str]
    file: Optional[EncryptedFile]
