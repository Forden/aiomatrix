import datetime
import typing
from typing import Optional

from pydantic import BaseModel

from aiomatrix.utils.mixins import ContextVarMixin

if typing.TYPE_CHECKING:
    from ...client import AiomatrixClient


class MatrixEventObject(BaseModel, ContextVarMixin):
    raw: Optional[dict]

    class Config:
        json_encoders = {datetime.datetime: lambda dt: int(dt.timestamp())}

    def __init__(self, **data):
        super().__init__(**data)
        self.raw = data

    @property
    def client(self) -> 'AiomatrixClient':
        from ...client import AiomatrixClient
        client = AiomatrixClient.get()
        if client is None:
            raise RuntimeError('Couldn\'t get client instance from context. Set it by AiomatrixClient.set(client)')
        return client
