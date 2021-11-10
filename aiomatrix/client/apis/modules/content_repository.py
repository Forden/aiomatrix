import io
import pathlib
from builtins import int
from typing import AsyncGenerator, BinaryIO, Optional, Union

import aiofiles as aiofiles

from aiomatrix import types, utils
from .. import raw_api


class ContentRepositoryAPI:
    def __init__(self, raw_api_client: raw_api.RawAPI):
        self._raw_api = raw_api_client

    async def get_config(self):
        await self._raw_api.make_request(
            'GET', f'_matrix/media/v3/config',
            model_type=types.responses.ContentRepositoryConfig
        )

    @classmethod
    async def __download_to_binary_io(
            cls, destination: BinaryIO, seek: bool, stream: AsyncGenerator[bytes, None]
    ) -> BinaryIO:
        async for chunk in stream:
            destination.write(chunk)
            destination.flush()
        if seek is True:
            destination.seek(0)
        return destination

    @classmethod
    async def __download_to_file(
            cls, destination: Union[str, pathlib.Path], stream: AsyncGenerator[bytes, None]
    ) -> None:
        async with aiofiles.open(destination, 'wb') as f:
            async for chunk in stream:
                await f.write(chunk)

    async def download_file(
            self, mxc_url: str, destination: Optional[Union[pathlib.Path, str]] = None, chunk_size: int = 65536
    ) -> Optional[BinaryIO]:
        if destination is None:
            destination = io.BytesIO()
        if mxc_url.startswith('mxc://'):
            mxc_url = mxc_url[6:]
        server_name, media_id = mxc_url.split('/')
        stream = self._raw_api.stream_response(f'_matrix/media/r0/download/{server_name}/{media_id}', chunk_size)
        try:
            if isinstance(destination, (str, pathlib.Path)):
                return await self.__download_to_file(destination, stream)
            else:
                return await self.__download_to_binary_io(destination, True, stream)
        finally:
            pass

    async def download_thumbnail(
            self, mxc_url: str, height: int, width: int, method: Union[str, types.misc.ResizingMethodsEnum],
            destination: Optional[Union[pathlib.Path, str]] = None, chunk_size: int = 65536,
    ) -> Optional[BinaryIO]:
        if destination is None:
            destination = io.BytesIO()
        if mxc_url.startswith('mxc://'):
            mxc_url = mxc_url[6:]
        server_name, media_id = mxc_url.split('/')
        payload = {
            'params': {
                'height': height,
                'width':  width,
                'method': method
            }
        }
        stream = self._raw_api.stream_response(
            f'_matrix/media/r0/thumbnail/{server_name}/{media_id}', chunk_size, **payload
        )
        try:
            if isinstance(destination, (str, pathlib.Path)):
                return await self.__download_to_file(destination, stream)
            else:
                return await self.__download_to_binary_io(destination, True, stream)
        finally:
            pass

    async def upload_file(self, file: Union[utils.InputFile, str]) -> types.responses.UploadedFileResponse:
        payload = {
            'data':    file.read(file.chunk_size),
            'params':  {
                           'filename': file.filename
                       } if file.filename is not None else {},
        }
        r = await self._raw_api.make_request(
            'POST', f'_matrix/media/r0/upload',
            model_type=types.responses.UploadedFileResponse, **payload
        )
        return r
