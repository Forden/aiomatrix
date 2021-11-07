import abc
import typing
import uuid

from aiomatrix import types

if typing.TYPE_CHECKING:
    from aiomatrix import AiomatrixClient


class BaseFilter(metaclass=abc.ABCMeta):
    def __init__(self):
        self.filter_id: str = f'{uuid.uuid4()}'

    @abc.abstractmethod
    async def check(self, event: types.events.BasicEvent, client: 'AiomatrixClient') -> bool:
        raise NotImplementedError
