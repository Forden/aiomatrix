from typing import List, Optional

from .. import models
from ..utils import raw_api


class SyncingAPI:
    def __init__(self, raw_api_client: raw_api.RawAPI):
        self._raw_api = raw_api_client
        self.state = dict

    async def sync(
            self, filter_id: Optional[str] = None, since: Optional[str] = None, full_state: bool = False,
            set_presence: models.modules.presence.PresenceEnum = models.modules.presence.PresenceEnum.online,
            timeout: int = 0
    ) -> models.SyncResponse:
        payload = {'params': {}}
        if filter_id is not None:
            payload['params']['filter'] = filter_id
        if since is not None:
            payload['params']['since'] = since
        if full_state is not None:
            payload['params']['full_state'] = full_state.__str__().lower()
        if set_presence is not None:
            payload['params']['set_presence'] = f'{set_presence}'
        if timeout is not None:
            payload['params']['timeout'] = timeout
        r = await self._raw_api.make_request(
            'GET', '_matrix/client/r0/sync', models.SyncResponse, **payload
        )
        return r

    async def get_room_event(self, room_id: str, event_id: str) -> models.events.RoomEvent:
        r = await self._raw_api.make_request(
            'GET', f'_matrix/client/r0/rooms/{room_id}/event/{event_id}', models.events.RoomEvent
        )
        return r

    async def get_room_state(self, room_id: str) -> List[models.events.RoomEvent]:
        r = await self._raw_api.make_request(
            'GET', f'_matrix/client/r0/rooms/{room_id}/state', models.events.RoomEvent
        )
        return r

    async def get_room_members(
            self, room_id: str, at: Optional[str] = None,
            membership: Optional[models.events.RoomMemberMembershipEnum] = None,
            not_membership: Optional[models.events.RoomMemberMembershipEnum] = None
    ) -> models.RoomMembersResponse:
        payload = {'params': {}}
        if at is not None:
            payload['params']['at'] = at
        if membership is not None:
            payload['params']['membership'] = f'{membership}'
        if not_membership is not None:
            payload['params']['not_membership'] = f'{not_membership}'
        r = await self._raw_api.make_request(
            'GET', f'_matrix/client/r0/rooms/{room_id}/members', models.RoomMembersResponse, **payload
        )
        return r

    async def get_room_messages(
            self, room_id: str, from_token: str, to: Optional[str] = None, direction: str = 'f', limit: int = 10,
            filter_id: Optional[str] = None
    ) -> models.RoomMessagesResponse:
        payload = {'params': {'from': from_token}}
        if to is not None:
            payload['params']['to'] = to
        if direction is not None:
            payload['params']['dir'] = direction
        if limit is not None:
            payload['params']['limit'] = limit
        if filter_id is not None:
            payload['params']['filter'] = filter_id
        r = await self._raw_api.make_request(
            'GET', f'_matrix/client/r0/rooms/{room_id}/messages', models.RoomMessagesResponse, **payload
        )
        return r
