import typing

import pydantic

from aiomatrix import types
from . import BaseFilter


class Handler(pydantic.BaseModel):
    callback: typing.Callable
    filters: typing.Optional[typing.List[BaseFilter]] = None  # placeholder

    class Config:
        arbitrary_types_allowed = True

    async def check(self, event: types.events.RoomEvent) -> bool:
        for event_filter in self.filters:
            check_result = await event_filter.check(event)
            if not check_result:
                return False
        return True
