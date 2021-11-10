import io
import os.path
import pathlib
from abc import ABC, abstractmethod
from typing import AsyncGenerator, AsyncIterator, Optional, Union

import aiofiles

DEFAULT_CHUNK_SIZE = 64 * 1024  # 64 KB


class InputFile(ABC):
    def __init__(self, filename: Optional[str] = None, chunk_size: int = DEFAULT_CHUNK_SIZE):
        self.filename = filename
        self.chunk_size = chunk_size

    @abstractmethod
    async def read(self, chunk_size: int) -> AsyncGenerator[bytes, None]:
        yield b""

    async def __aiter__(self) -> AsyncIterator[bytes]:
        async for chunk in self.read(self.chunk_size):
            yield chunk


class FSInputFile(InputFile):
    def __init__(
            self, path: Union[pathlib.Path, str], filename: Optional[str] = None, chunk_size: int = DEFAULT_CHUNK_SIZE
    ):
        if filename is None:
            filename = os.path.basename(path)
        super().__init__(filename, chunk_size)
        self.path = path

    async def read(self, chunk_size: int) -> AsyncGenerator[bytes, None]:
        async with aiofiles.open(self.path, 'rb') as f:
            chunk = await f.read(chunk_size)
            while chunk:
                yield chunk
                chunk = await f.read(chunk_size)


class BufferedInputFile(InputFile):
    def __init__(self, data: Union[io.BytesIO, bytes], filename: Optional[str] = None, chunk_size: int = DEFAULT_CHUNK_SIZE):
        super().__init__(filename, chunk_size)
        self.data = data if isinstance(data, bytes) else data.getvalue()

    async def read(self, chunk_size: int) -> AsyncGenerator[bytes, None]:
        buffer = io.BytesIO(self.data)
        chunk = buffer.read(chunk_size)
        while chunk:
            yield chunk
            chunk = buffer.read(chunk_size)
