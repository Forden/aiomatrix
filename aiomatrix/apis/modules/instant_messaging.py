from typing import Optional

from ..syncing import SyncingAPI
from ... import types


def _add_reply(content: dict, reply_to: types.primitives.EventID):
    content['m.relates_to'] = {
        'm.in_reply_to': {
            'event_id': reply_to
        }
    }
    return content


class InstantMessagingAPI:
    def __init__(self, sync_api_client: SyncingAPI):
        self._sync_client = sync_api_client

    async def send_message(
            self, room_id: types.primitives.RoomID, text: str, reply_to: Optional[types.primitives.EventID] = None
    ) -> types.responses.SentEventResponse:
        content = {
            'body':    text,
            'msgtype': types.misc.RoomMessageEventMsgTypesEnum.text
        }
        if reply_to is not None:
            content = _add_reply(content, reply_to)
        r = await self._sync_client.send_message_event(room_id, types.misc.RoomEventTypesEnum.room_message, content)
        return r

    async def send_notice(
            self, room_id: types.primitives.RoomID, text: str, reply_to: Optional[types.primitives.EventID] = None
    ) -> types.responses.SentEventResponse:
        content = {
            'body':    text,
            'msgtype': types.misc.RoomMessageEventMsgTypesEnum.notice
        }
        if reply_to is not None:
            content = _add_reply(content, reply_to)
        r = await self._sync_client.send_message_event(room_id, types.misc.RoomEventTypesEnum.room_message, content)
        return r
