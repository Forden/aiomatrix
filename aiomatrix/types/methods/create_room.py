from typing import Any

import pydantic


class InitialState(pydantic.BaseModel):
    type: str
    state_key: str = ''
    content: Any


class Invite3PID(pydantic.BaseModel):
    id_server: str
    id_access_token: str
    medium: str
    address: str
