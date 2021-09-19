from typing import Any, List

import pydantic

class Event(pydantic.BaseModel):
    content: Any
    sender: str
    type: str


class ToDevice(pydantic.BaseModel):
    events: List[Event]