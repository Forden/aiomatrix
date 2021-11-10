from typing import Optional

from pydantic import BaseModel, Field


class ContentRepositoryConfig(BaseModel):
    upload_size: Optional[int] = Field(None, alias='m.upload.size')


class UploadedFileResponse(BaseModel):
    content_uri: str
