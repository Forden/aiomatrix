from aiomatrix import types
from aiomatrix.utils import quotes, raw_api


class TypingNotifications:
    def __init__(self, raw_api_client: raw_api.RawAPI):
        self._raw_api = raw_api_client

    async def send_typing(
            self, user_id: types.primitives.UserID, room_id: types.primitives.RoomID, timeout: int
    ):
        payload = {
            'data': {
                'timeout': timeout
            }
        }
        await self._raw_api.make_request(
            'PUT', f'_matrix/client/r0/rooms/{room_id}/typing/{quotes.quote_user_id(user_id)}',
            **payload
        )

    async def send_typing_status(
            self, user_id: types.primitives.UserID, room_id: types.primitives.RoomID, status: bool
    ):
        payload = {
            'data': {
                'status': status
            }
        }
        await self._raw_api.make_request(
            'PUT', f'_matrix/client/r0/rooms/{room_id}/typing/{quotes.quote_user_id(user_id)}',
            **payload
        )
