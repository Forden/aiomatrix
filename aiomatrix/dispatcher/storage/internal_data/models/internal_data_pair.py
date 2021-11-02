import pydantic


class InternalDataPair(pydantic.BaseModel):
    key: str
    data: str
