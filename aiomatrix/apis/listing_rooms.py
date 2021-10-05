from typing import Optional

from .. import types
from ..utils import raw_api


class ListingRoomsAPI:
    def __init__(self, raw_api_client: raw_api.RawAPI):
        self._raw_api = raw_api_client

    async def get_room_visibility(self, room_id: types.primitives.RoomID) -> types.responses.RoomVisibilityResponse:
        r = await self._raw_api.make_request(
            'GET', f'_matrix/client/r0/directory/list/room/{room_id}', model_type=types.responses.RoomVisibilityResponse
        )
        return r

    async def set_room_visibility(self, room_id: types.primitives.RoomID, visibility: types.misc.RoomVisiblityEnum):
        payload = {
            'data': {
                'visibility': f'{visibility}'
            }
        }
        await self._raw_api.make_request(
            'PUT', f'_matrix/client/r0/directory/list/room/{room_id}', model_type=None, **payload
        )

    async def get_server_public_rooms(
            self, limit: Optional[int] = None, since: Optional[str] = None, server: Optional[str] = None
    ) -> types.responses.ServerPublicRoomsResponse:
        payload = {'params': {}}
        if limit is not None:
            payload['params']['limit'] = limit
        if since is not None:
            payload['params']['since'] = since
        if server is not None:
            payload['params']['server'] = server
        r = await self._raw_api.make_request(
            'GET', f'_matrix/client/r0/publicRooms', model_type=types.responses.ServerPublicRoomsResponse, **payload
        )
        return r

    async def get_server_all_public_rooms(
            self, server: Optional[str] = None
    ) -> types.responses.ServerPublicRoomsResponse:
        result = types.responses.ServerPublicRoomsResponse(chunk=[])
        step = 250
        since = None
        while True:
            server_rooms_chunk = await self.get_server_public_rooms(step, since, server)
            result.total_room_count_estimate = server_rooms_chunk.total_room_count_estimate
            result.chunk.extend(server_rooms_chunk.chunk)
            if server_rooms_chunk.next_batch is None:
                break
            else:
                since = server_rooms_chunk.next_batch
        return result
