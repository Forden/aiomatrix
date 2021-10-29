from enum import Enum


class RoomVisiblityEnum(str, Enum):
    public = 'public'
    private = 'private'


class CreateRoomPresetEnum(str, Enum):
    public_chat = 'public_chat'
    private_chat = 'private_chat'
    trusted_private_chat = 'trusted_private_chat'


class RoomStabilityEnum(str, Enum):
    stable = 'stable'
    unstable = 'unstable'


class RoomEventTypesEnum(str, Enum):
    room_message = 'm.room.message'
    room_member = 'm.room.member'
    reaction = 'm.reaction'
    redaction = 'm.room.redaction'


class RoomMessageEventMsgTypesEnum(str, Enum):
    text = 'm.text'
    emote = 'm.emote'  # looks unused, replaced with m.reaction
    reaction = 'm.reaction'
    notice = 'm.notice'
    image = 'm.image'
    file = 'm.file'
    audio = 'm.audio'
    location = 'm.location'
    video = 'm.video'


class PresenceEnum(str, Enum):
    offline = 'offline'
    online = 'online'
    unavailable = 'unavailable'
