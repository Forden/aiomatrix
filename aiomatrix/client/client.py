import json
import typing
from typing import Optional, Tuple, Union

from . import apis
from .apis import raw_api
from .. import types


class AiomatrixClient:
    def __init__(self, server_url: str, auth_details: Tuple[str, dict]):
        self.server_url = server_url
        self._auth_cb = {'password': self.login_by_password}[auth_details[0]]
        self._auth_details = auth_details[1]
        self._raw_api = raw_api.RawAPI(self.server_url)
        self.auth_api = apis.AuthAPI(self._raw_api)
        self.capabilities_api = apis.CapabilitiesAPI(self._raw_api)
        self.room_api = apis.RoomsAPI(self._raw_api)
        self.room_membership_api = apis.RoomMembershipAPI(self._raw_api)
        self.listing_room_api = apis.ListingRoomsAPI(self._raw_api)
        self.sync_api = apis.SyncingAPI(self._raw_api)

        self.presence_api = apis.modules.PresenceAPI(self._raw_api)
        self.instant_messaging_api = apis.modules.InstantMessagingAPI(self.sync_api)
        self.typing_notifications_api = apis.modules.TypingNotifications(self._raw_api)

        self.me: typing.Optional[types.responses.WhoAmIResponse] = None

    async def login(self):
        if not self._raw_api.is_authorized:
            login_result = await self._auth_cb(**self._auth_details)
            if login_result:
                self.me = await self.auth_api.whoami()

    async def login_by_password(self, login: str, password: str, device_id: Optional[str] = None) -> bool:
        supported_login_types = await self.auth_api.get_login_types()
        support_password_auth = 'm.login.password' in map(lambda x: x.type, supported_login_types.flows)
        if support_password_auth:
            login_response = await self.auth_api.password_login(login, password, device_id)
            if login_response.access_token:
                self.auth_api.set_access_token(login_response.access_token)
                return True
        return False

    @staticmethod
    def parse_event(
            event: Union[types.events.RoomEvent, types.events.RoomStateEvent]
    ) -> Union[types.events.RoomEvent, types.events.RoomMessageEvent, types.events.RoomRedactionEvent]:
        if isinstance(event, types.events.RoomEvent):
            if event.unsigned.redacted_because is not None:
                # dirty hack to get to original event filed names
                event = types.events.RoomRedactionEvent(**json.loads(event.json(by_alias=True)))
                event.unsigned.redacted_because = types.events.RoomRedactionEvent(**event.unsigned.redacted_because)
                return event
            if event.type == types.misc.RoomEventTypesEnum.room_message:
                if event.content is not None:
                    message_event_content = types.events.BasicRoomMessageEventContent(**event.content)
                    msgtypes = {
                        types.misc.RoomMessageEventMsgTypesEnum.audio:    types.modules.instant_messaging.AudioContent,
                        types.misc.RoomMessageEventMsgTypesEnum.emote:    types.modules.instant_messaging.EmoteContent,
                        types.misc.RoomMessageEventMsgTypesEnum.file:     types.modules.instant_messaging.FileContent,
                        types.misc.RoomMessageEventMsgTypesEnum.image:    types.modules.instant_messaging.ImageContent,
                        types.misc.RoomMessageEventMsgTypesEnum.location: types.modules.instant_messaging.LocationContent,
                        types.misc.RoomMessageEventMsgTypesEnum.notice:   types.modules.instant_messaging.NoticeContent,
                        types.misc.RoomMessageEventMsgTypesEnum.text:     types.modules.instant_messaging.TextContent,
                        types.misc.RoomMessageEventMsgTypesEnum.video:    types.modules.instant_messaging.VideoContent,
                    }
                    if message_event_content.msgtype in msgtypes:
                        event.content = msgtypes[message_event_content.msgtype](**message_event_content.raw)
                    if message_event_content.new_content and message_event_content.new_content.msgtype in msgtypes:
                        event.content.new_content = msgtypes[message_event_content.new_content.msgtype](
                            **message_event_content.new_content.raw
                        )
            elif event.type == types.misc.RoomEventTypesEnum.reaction:
                if event.content:
                    event.content = types.events.relationships.ReactionRelationshipContent(**event.content)
        elif isinstance(event, types.events.RoomStateEvent):
            print(event)
        return event
