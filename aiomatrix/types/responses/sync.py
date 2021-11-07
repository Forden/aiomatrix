from typing import Dict, List, Optional

import pydantic
from pydantic import Field

from ..events import BasicEvent, RoomEvent, RoomStateEvent, modules
from ..primitives import EventID, RoomID, UserID


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


class Event(BasicEvent):
    sender: UserID


class StrippedStateEvent(Event):
    state_key: str


class InviteState(pydantic.BaseModel):
    events: List[StrippedStateEvent]


class InvitedRooms(pydantic.BaseModel):
    invite_state: InviteState


class LeftRooms(pydantic.BaseModel):
    state: State
    timeline: Timeline
    account_data: AccountData


class Rooms(pydantic.BaseModel):
    join: Optional[Dict[RoomID, JoinedRooms]]
    invite: Optional[Dict[RoomID, InvitedRooms]]
    leave: Optional[Dict[RoomID, LeftRooms]]


class SyncResponse(pydantic.BaseModel):
    next_batch: str
    rooms: Optional[Rooms]
    presence: Optional[Presence]
    account_data: Optional[AccountData]
    to_device: Optional[modules.send_to_device.ToDevice]
    device_lists: Optional[modules.e2ee.DeviceLists]
    device_one_time_keys_count: Optional[Dict[str, int]]


class SentEventResponse(pydantic.BaseModel):
    event_id: EventID
