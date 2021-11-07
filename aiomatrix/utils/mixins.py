# noinspection PyPackageRequirements
import contextvars
import typing
from typing import Type, TypeVar

if typing.TYPE_CHECKING:
    from aiomatrix import AiomatrixClient

T = TypeVar('T')


class ContextVarMixin:
    def __init_subclass__(cls, **kwargs):
        cls.__context_instance = contextvars.ContextVar(f'instance_{cls.__name__}')
        return cls

    @classmethod
    def get(cls: Type[T], no_error=True) -> T:
        if no_error:
            return cls.__context_instance.get(None)
        return cls.__context_instance.get()

    @classmethod
    def set(cls: Type[T], value: T):
        if not isinstance(value, cls):
            raise TypeError(f'Value should be instance of {cls.__name__!r} not {type(value).__name__!r}')
        cls.__context_instance.set(value)


class ContextClientMixin:
    @property
    def client(self) -> 'AiomatrixClient':
        from ..client import AiomatrixClient
        client = AiomatrixClient.get()
        if client is None:
            raise RuntimeError('Couldn\'t get client instance from context. Set it by AiomatrixClient.set(client)')
        return client
