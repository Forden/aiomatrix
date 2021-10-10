from typing import NewType

RoomID = NewType('RoomID', str)
RoomAlias = NewType('RoomAlias', str)

UserID = NewType('UserID', str)
EventID = NewType('EventID', str)

EventContent = NewType('EventContent', dict)
