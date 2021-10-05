from aiomatrix import types


class BaseFilter:
    def check(self, event: types.events.RoomEvent):
        raise NotImplementedError
