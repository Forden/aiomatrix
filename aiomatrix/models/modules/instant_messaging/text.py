from typing import Optional

from ...events.basic import BasicRoomMessageEventContent, RoomMessageEventMsgTypesEnum


class Text(BasicRoomMessageEventContent):
    msgtype: RoomMessageEventMsgTypesEnum = RoomMessageEventMsgTypesEnum.text
    format: Optional[str]
    formatted_body: Optional[str]
