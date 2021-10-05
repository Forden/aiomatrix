from typing import List

import pydantic


class LoginFlow(pydantic.BaseModel):
    type: str


class SupportedLoginTypes(pydantic.BaseModel):
    flows: List[LoginFlow]
