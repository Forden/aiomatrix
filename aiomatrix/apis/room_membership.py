from typing import List, Optional, Union

from .. import types
from ..utils import raw_api


class RoomMembershipAPI:
    def __init__(self, raw_api_client: raw_api.RawAPI):
        self._raw_api = raw_api_client

    async def get_user_joined_rooms(self) -> types.responses.UserJoinedRoomsResponse:
        r = await self._raw_api.make_request(
            'GET', f'_matrix/client/r0/joined_rooms', model_type=types.responses.UserJoinedRoomsResponse
        )
        return r

    async def invite_to_room(self, room_id: types.primitives.RoomID, user_id: types.primitives.UserID):
        payload = {
            'data': {
                'user_id': user_id
            }
        }
        await self._raw_api.make_request(
            'POST', f'_matrix/client/r0/rooms/{room_id}/invite', model_type=None, **payload
        )

    async def join_room_by_id(
            self, room_id: types.primitives.RoomID,
            third_party_signed: Optional[types.methods.join_room_query.ThirdPartySigned] = None
    ) -> types.responses.UserJoinRoomResponse:
        payload = {'data': {}}
        if third_party_signed is not None:
            payload['data']['third_party_signed'] = third_party_signed.dict()
        r = await self._raw_api.make_request(
            'POST', f'_matrix/client/r0/rooms/{room_id}/join', model_type=types.responses.UserJoinRoomResponse,
            **payload
        )
        return r

    async def join_room(
            self, room_id_or_alias: Union[types.primitives.RoomID, types.primitives.RoomAlias],
            servers: Optional[List[str]] = None,
            third_party_signed: Optional[types.methods.join_room_query.ThirdPartySigned] = None
    ) -> types.responses.UserJoinRoomResponse:
        payload = {'data': {}, 'params': {}}
        if third_party_signed is not None:
            payload['data']['third_party_signed'] = third_party_signed.dict()
        if servers is not None:
            payload['params'] = [('server_name', i) for i in servers]
        r = await self._raw_api.make_request(
            'POST', f'_matrix/client/r0/join/{room_id_or_alias}', model_type=types.responses.UserJoinRoomResponse,
            **payload
        )
        return r

    async def leave_room(self, room_id: types.primitives.RoomID):
        await self._raw_api.make_request('POST', f'_matrix/client/r0/rooms/{room_id}/leave')

    async def forget_room(self, room_id: types.primitives.RoomID):
        await self._raw_api.make_request('POST', f'_matrix/client/r0/rooms/{room_id}/forget')

    async def kick_from_room(
            self, room_id: types.primitives.RoomID, user_id: types.primitives.UserID, reason: Optional[str] = None
    ):
        payload = {
            'data': {
                'user_id': user_id
            }
        }
        if reason is not None:
            payload['data']['reason'] = reason
        await self._raw_api.make_request(
            'POST', f'_matrix/client/r0/rooms/{room_id}/kick', model_type=None, **payload
        )

    async def ban_from_room(
            self, room_id: types.primitives.RoomID, user_id: types.primitives.UserID, reason: Optional[str] = None
    ):
        payload = {
            'data': {
                'user_id': user_id
            }
        }
        if reason is not None:
            payload['data']['reason'] = reason
        await self._raw_api.make_request(
            'POST', f'_matrix/client/r0/rooms/{room_id}/ban', model_type=None, **payload
        )

    async def unban_in_room(self, room_id: types.primitives.RoomID, user_id: types.primitives.UserID):
        payload = {
            'data': {
                'user_id': user_id
            }
        }
        await self._raw_api.make_request(
            'POST', f'_matrix/client/r0/rooms/{room_id}/unban', model_type=None, **payload
        )
