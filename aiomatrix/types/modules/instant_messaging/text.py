from typing import Optional

from ...events.base import BasicRoomMessageEventContent


class TextContent(BasicRoomMessageEventContent):
    format: Optional[str]
    formatted_body: Optional[str]
