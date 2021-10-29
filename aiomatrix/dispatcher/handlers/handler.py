import typing

import pydantic

from aiomatrix import types
from aiomatrix.dispatcher.filters import BaseFilter

if typing.TYPE_CHECKING:
    from aiomatrix import AiomatrixClient


class Handler(pydantic.BaseModel):
    callback: typing.Callable
    filters: typing.Optional[typing.List[BaseFilter]] = None  # placeholder

    class Config:
        arbitrary_types_allowed = True

    async def check(self, event: types.events.RoomEvent, client: 'AiomatrixClient') -> bool:
        for event_filter in self.filters:
            check_result = await event_filter.check(event, client)
            if not check_result:
                return False
        return True
