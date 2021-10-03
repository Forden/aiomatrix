from typing import Dict, List, Optional

import pydantic
from pydantic import Field

from . import modules
from .events import BasicEvent, RoomEvent, RoomMember, RoomStateEvent, StrippedState


class RoomSummary(pydantic.BaseModel):
    heroes: Optional[List[str]] = Field(None, alias='m.heroes')
    joined_member_count: Optional[int] = Field(None, alias='m.joined_member_count')
    invited_member_count: Optional[int] = Field(None, alias='m.invited_member_count')


class UnreadNotifications(pydantic.BaseModel):
    highlight_count: int
    notification_count: int


class Timeline(pydantic.BaseModel):
    events: List[RoomEvent]
    limited: bool
    prev_batch: str


class State(pydantic.BaseModel):
    events: List[RoomStateEvent]


class AccountData(pydantic.BaseModel):
    events: List[BasicEvent]


class Presence(pydantic.BaseModel):
    events: List[modules.presence.PresenceEvent]


class Ephemeral(pydantic.BaseModel):
    events: List[BasicEvent]


class JoinedRooms(pydantic.BaseModel):
    summary: Optional[RoomSummary]
    state: Optional[State]
    timeline: Optional[Timeline]
    ephemeral: Optional[Ephemeral]
    account_data: Optional[AccountData]
    unread_notifications: Optional[UnreadNotifications]


class InviteState(pydantic.BaseModel):
    events: List[StrippedState]


class InvitedRooms(pydantic.BaseModel):
    invite_state: InviteState


class LeftRooms(pydantic.BaseModel):
    state: State
    timeline: Timeline
    account_data: AccountData


class Rooms(pydantic.BaseModel):
    join: Optional[Dict[str, JoinedRooms]]
    invite: Optional[Dict[str, InvitedRooms]]
    leave: Optional[Dict[str, LeftRooms]]


class SyncResponse(pydantic.BaseModel):
    next_batch: str
    rooms: Optional[Rooms]
    presence: Optional[Presence]
    account_data: Optional[AccountData]
    to_device: Optional[modules.send_to_device.ToDevice]
    device_lists: Optional[modules.e2ee.DeviceLists]
    device_one_time_keys_count: Optional[Dict[str, int]]


class RoomMembersResponse(pydantic.BaseModel):
    chunk: List[RoomMember]


class RoomMessagesResponse(pydantic.BaseModel):
    start: str
    end: str
    chunk: List[RoomEvent]
    state: List[RoomStateEvent]