from typing import Any, List

import pydantic

from aiomatrix.types import primitives


class ToDeviceEvent(pydantic.BaseModel):
    content: Any
    sender: primitives.UserID
    type: str


class ToDevice(pydantic.BaseModel):
    events: List[ToDeviceEvent]
