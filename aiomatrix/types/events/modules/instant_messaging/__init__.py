from __future__ import annotations

from .audio import AudioContent
from .emote import EmoteContent
from .file import FileContent
from .image import ImageContent
from .location import LocationContent
from .new_content import NewContent
from .notice import NoticeContent
from .text import TextContent
from .video import VideoContent

__all__ = [
    'TextContent',
    'NoticeContent',
    'EmoteContent',
    'AudioContent',
    'FileContent',
    'ImageContent',
    'LocationContent',
    'VideoContent',
    'NewContent'
]

for _entity_name in __all__:
    _entity = globals()[_entity_name]
    if not hasattr(_entity, "update_forward_refs"):
        continue
    _entity.update_forward_refs(**globals())

del _entity
del _entity_name
