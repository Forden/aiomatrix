import abc

from aiomatrix import types


class BaseFilter(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def check(self, event: types.events.BasicEvent):
        raise NotImplementedError
