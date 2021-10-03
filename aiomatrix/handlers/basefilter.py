import aiomatrix.models.events


class BaseFilter:
    def check(self, event: aiomatrix.models.events.RoomEvent):
        raise NotImplementedError
