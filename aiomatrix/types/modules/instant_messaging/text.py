from typing import Optional

from ...events import BasicRoomMessageEventContent


class TextContent(BasicRoomMessageEventContent):
    format: Optional[str]
    formatted_body: Optional[str]
