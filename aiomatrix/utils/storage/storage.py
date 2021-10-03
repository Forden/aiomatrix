from . import BasePresenceStorage, BaseStateStorage


class StorageRepo:
    def __init__(self, state_storage: BaseStateStorage, presence_storage: BasePresenceStorage):
        self.state_storage = state_storage
        self.presence_storage = presence_storage
