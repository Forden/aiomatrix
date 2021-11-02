from aiomatrix import types


class BaseRoomsStorage:
    async def setup(self):
        raise NotImplementedError

    async def get_room_data(self, room_id: types.primitives.RoomID):
        pass
