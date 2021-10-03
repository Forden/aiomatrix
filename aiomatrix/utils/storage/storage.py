from . import BasePresenceStorage, BaseStateStorage
from .presence import PresenceRepo
from .state import StateRepo


class StorageRepo:
    def __init__(self, state_storage: BaseStateStorage, presence_storage: BasePresenceStorage):
        self.state_repo = StateRepo(state_storage)
        self.presence_storage = PresenceRepo(presence_storage)
