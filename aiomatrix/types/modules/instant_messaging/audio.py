from typing import Optional

import pydantic

from .basic_file_info import BasicFileInfo
from ..e2ee import EncryptedFile
from ...events.base import BasicRoomMessageEventContent


class AudioInfo(BasicFileInfo, pydantic.BaseModel):
    duration: int


class AudioContent(BasicRoomMessageEventContent):
    info: Optional[AudioInfo]
    url: Optional[str]
    file: Optional[EncryptedFile]
