import inspect
import typing

import pydantic
from pydantic import root_validator

from aiomatrix import types
from aiomatrix.dispatcher.filters import BaseFilter

if typing.TYPE_CHECKING:
    from aiomatrix import AiomatrixClient


class HandlerCallback(pydantic.BaseModel):
    callback: typing.Callable
    spec: typing.Optional[inspect.FullArgSpec] = None

    @root_validator(pre=True)
    def _parse_spec(cls, values: dict):
        values['spec'] = inspect.getfullargspec(values['callback'])
        return values


class Handler(pydantic.BaseModel):
    callback: HandlerCallback
    filters: typing.Tuple[BaseFilter, ...]

    class Config:
        arbitrary_types_allowed = True

    async def check(self, event: types.events.RoomEvent, client: 'AiomatrixClient') -> bool:
        for event_filter in self.filters:
            check_result = await event_filter.check(event, client)
            if not check_result:
                return False
        return True
