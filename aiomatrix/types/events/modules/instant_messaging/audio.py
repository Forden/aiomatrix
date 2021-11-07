from __future__ import annotations

from typing import Optional

from .basic_file_info import BasicFileInfo
from ..e2ee import EncryptedFile
from ...base_room_events import BaseMessageEventContent


class AudioInfo(BasicFileInfo):
    duration: int


class AudioContent(BaseMessageEventContent):
    msgtype: str = 'm.audio'
    info: Optional[AudioInfo]
    url: Optional[str]
    file: Optional[EncryptedFile]
