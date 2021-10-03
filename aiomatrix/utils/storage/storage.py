from . import BaseInternalDataStorage, BasePresenceStorage, BaseStateStorage
from .internal_data import InternalDataRepo
from .presence import PresenceRepo
from .state import StateRepo


class StorageRepo:
    def __init__(
            self, internal_storage: BaseInternalDataStorage, state_storage: BaseStateStorage,
            presence_storage: BasePresenceStorage
    ):
        self.internal_repo = InternalDataRepo(internal_storage)
        self.state_repo = StateRepo(state_storage)
        self.presence_storage = PresenceRepo(presence_storage)
