from __future__ import annotations

import typing

from ..filters import BaseFilter
from ..handlers import Handler, HandlerCallback
from ...client import AiomatrixClient
from ...types.events import BaseMessageEventContent, RoomEvent, RoomMessageEvent, RoomStateContent, RoomStateEvent
from ...types.events.modules.instant_messaging import NewContent


def _clear_filters(filters: typing.Tuple[BaseFilter]) -> typing.Tuple[BaseFilter]:
    """
    removing repeating filters from list
    """
    result = {}
    for i in filters:
        result[i.filter_id] = i
    return tuple(result.values())


class MatrixEventsObserver:
    def __init__(self):
        self.handlers: typing.List[Handler] = []

    def register(self, callback: typing.Callable, *filters: BaseFilter):
        _filters = _clear_filters(tuple(filters))
        self.handlers.append(
            Handler(
                callback=HandlerCallback(callback=callback),
                filters=_filters
            )
        )

    async def trigger(self, event: typing.Union[RoomEvent, RoomMessageEvent, RoomStateEvent], client: AiomatrixClient):
        additional_args: typing.Dict[
            str, typing.Optional[typing.Union[AiomatrixClient, BaseMessageEventContent, RoomStateContent]]
        ] = {}
        for handler in self.handlers:
            if await handler.check(event, client):
                for arg, annotation in handler.callback.spec.annotations.items():
                    if annotation == AiomatrixClient:
                        additional_args[arg] = client
                    elif arg == 'content':
                        additional_args['content'] = event.content
                    elif arg == 'new_content':
                        if isinstance(event, RoomMessageEvent) and isinstance(event.content, NewContent):
                            additional_args[arg] = event.content.new_content
                        else:
                            additional_args[arg] = None
                await handler.callback.callback(event, **additional_args)
