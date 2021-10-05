from typing import List, Optional

from .. import types
from ..utils import raw_api


class RoomsAPI:
    def __init__(self, raw_api_client: raw_api.RawAPI):
        self._raw_api = raw_api_client

    async def create_room(
            self, room_alias: types.primitives.RoomAlias,
            visibility: Optional[types.misc.RoomVisiblityEnum] = types.misc.RoomVisiblityEnum.private,
            preset: Optional[types.misc.CreateRoomPresetEnum] = None, is_direct: bool = False,
            room_name: Optional[str] = None, topic: Optional[str] = None, invite: Optional[List[str]] = None,
            invite_3pid: Optional[List[types.methods.create_room.Invite3PID]] = None,
            room_version: Optional[str] = None, creation_content: Optional[dict] = None,
            initial_state: Optional[types.methods.create_room.InitialState] = None
    ) -> types.responses.CreateRoomResponse:
        payload = {
            'data': {
                'room_alias_name': room_alias,
                'is_direct':       is_direct
            }
        }
        if visibility is not None:
            payload['data']['visibility'] = f'{visibility}'
        if preset is not None:
            payload['data']['preset'] = f'{preset}'
        if room_name is not None:
            payload['data']['name'] = room_name
        if topic is not None:
            payload['data']['topic'] = topic
        if invite is not None:
            payload['data']['invite'] = invite
        if invite_3pid is not None:
            payload['data']['invite_3pid'] = invite_3pid
        if room_version is not None:
            payload['data']['room_version'] = room_version
        if creation_content is not None:
            payload['data']['creation_content'] = creation_content
        if initial_state is not None:
            payload['data']['initial_state'] = initial_state
        r = await self._raw_api.make_request(
            'POST', '_matrix/client/r0/createRoom', model_type=types.responses.CreateRoomResponse, **payload
        )
        return r

    async def add_new_alias(self, room_id: types.primitives.RoomID, room_alias: str):
        payload = {
            'data': {
                'room_id': room_id
            }
        }
        await self._raw_api.make_request(
            'PUT', f'_matrix/client/r0/directory/room/{room_alias}', model_type=None, **payload
        )

    async def resolve_room_alias(
            self, room_alias: types.primitives.RoomAlias
    ) -> types.responses.ResolveRoomAliasResponse:
        r = await self._raw_api.make_request(
            'GET', f'_matrix/client/r0/directory/room/{room_alias}', model_type=types.responses.ResolveRoomAliasResponse
        )
        return r

    async def delete_room_alias(self, room_alias: types.primitives.RoomAlias):
        await self._raw_api.make_request('DELETE', f'_matrix/client/r0/directory/room/{room_alias}')

    async def get_room_aliases(self, room_id: types.primitives.RoomID) -> types.responses.GetRoomAliasesResponse:
        r = await self._raw_api.make_request(
            'GET', f'_matrix/client/r0/rooms/{room_id}/aliases', model_type=types.responses.GetRoomAliasesResponse
        )
        return r
