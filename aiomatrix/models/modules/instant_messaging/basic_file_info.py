import pydantic


class BasicFileInfo(pydantic.BaseModel):
    mimetype: str
    size: int
