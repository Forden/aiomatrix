from typing import Optional

from . import models


class BaseInternalDataStorage:
    async def get_last_sync_token(self) -> Optional[models.InternalDataPair]:
        raise NotImplementedError

    async def set_last_sync_token(self, token: str):
        raise NotImplementedError
