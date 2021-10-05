from typing import Optional

from ...events.base import BasicRoomMessageEventContent
from ...misc import RoomMessageEventMsgTypesEnum


class TextContent(BasicRoomMessageEventContent):
    msgtype: RoomMessageEventMsgTypesEnum = RoomMessageEventMsgTypesEnum.text
    format: Optional[str]
    formatted_body: Optional[str]
