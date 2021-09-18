from typing import List, Optional

from .. import models
from ..utils import raw_api


class RoomMembershipAPI:
    def __init__(self, raw_api_client: raw_api.RawAPI):
        self._raw_api = raw_api_client

    async def get_user_joined_rooms(self) -> models.UserJoinedRoomsResponse:
        r = await self._raw_api.make_request(
            'GET', f'_matrix/client/r0/joined_rooms', models.UserJoinedRoomsResponse
        )
        return r

    async def invite_to_room(self, room_id: str, user_id: str):
        payload = {
            'data': {
                'user_id': user_id
            }
        }
        await self._raw_api.make_request(
            'POST', f'_matrix/client/r0/rooms/{room_id}/invite', None, **payload
        )

    async def join_room(
            self, room_id: str, third_party_signed: Optional[models.UserJoinRoomThirdPartSigned] = None
    ) -> models.UserJoinRoomResponse:
        payload = {'data': {}}
        if third_party_signed is not None:
            payload['data']['third_party_signed'] = third_party_signed.dict()
        r = await self._raw_api.make_request(
            'POST', f'_matrix/client/r0/rooms/{room_id}/join', models.UserJoinRoomResponse, **payload
        )
        return r

    async def join_room_through(
            self, room_id_or_alias: str, servers: List[str],
            third_party_signed: Optional[models.UserJoinRoomThirdPartSigned] = None
    ) -> models.UserJoinedRoomsResponse:
        payload = {'data': {}, 'params': {'servers': servers}}
        if third_party_signed is not None:
            payload['data']['third_party_signed'] = third_party_signed.dict()
        r = await self._raw_api.make_request(
            'POST', f'_matrix/client/r0/join/{room_id_or_alias}', models.UserJoinRoomResponse, **payload
        )
        return r

    async def leave_room(self, room_id: str):
        await self._raw_api.make_request('POST', f'_matrix/client/r0/rooms/{room_id}/leave')

    async def forget_room(self, room_id: str):
        await self._raw_api.make_request('POST', f'_matrix/client/r0/rooms/{room_id}/forget')

    async def kick_from_room(self, room_id: str, user_id: str, reason: Optional[str] = None):
        payload = {
            'data': {
                'user_id': user_id
            }
        }
        if reason is not None:
            payload['data']['reason'] = reason
        await self._raw_api.make_request(
            'POST', f'_matrix/client/r0/rooms/{room_id}/kick', None, **payload
        )

    async def ban_from_room(self, room_id: str, user_id: str, reason: Optional[str] = None):
        payload = {
            'data': {
                'user_id': user_id
            }
        }
        if reason is not None:
            payload['data']['reason'] = reason
        await self._raw_api.make_request(
            'POST', f'_matrix/client/r0/rooms/{room_id}/ban', None, **payload
        )

    async def unban_in_room(self, room_id: str, user_id: str):
        payload = {
            'data': {
                'user_id': user_id
            }
        }
        await self._raw_api.make_request(
            'POST', f'_matrix/client/r0/rooms/{room_id}/unban', None, **payload
        )
