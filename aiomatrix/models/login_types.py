from typing import List

import pydantic


class LoginFlow(pydantic.BaseModel):
    type: str


class LoginTypes(pydantic.BaseModel):
    flows: List[LoginFlow]
