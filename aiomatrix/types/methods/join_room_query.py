import pydantic

from .. import primitives


class ThirdPartySigned(pydantic.BaseModel):
    sender: primitives.UserID
    mxid: str
    token: str
    signatures: dict
