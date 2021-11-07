from __future__ import annotations

from typing import Optional

from ...base_room_events import BaseMessageEventContent


class TextContent(BaseMessageEventContent):
    format: Optional[str]
    formatted_body: Optional[str]
