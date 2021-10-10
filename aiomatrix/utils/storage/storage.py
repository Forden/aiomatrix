from . import BaseInternalDataStorage, BasePresenceStorage, BaseEventStorage
from .internal_data import InternalDataRepo
from .presence import PresenceRepo
from .room_events import EventsRepo


class StorageRepo:
    def __init__(
            self, internal_storage: BaseInternalDataStorage, events_storage: BaseEventStorage,
            presence_storage: BasePresenceStorage
    ):
        self.internal_repo = InternalDataRepo(internal_storage)
        self.events_repo = EventsRepo(events_storage)
        self.presence_storage = PresenceRepo(presence_storage)
