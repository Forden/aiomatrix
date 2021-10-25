import asyncio
import json
import urllib.parse
from typing import Dict, List, Optional, Type, TypeVar, Union

import aiohttp
import pydantic

from aiomatrix import exceptions, loggers

T = TypeVar('T')


def canonical_json_dumps(value) -> bytes:
    return json.dumps(
        value,
        # Encode code-points outside of ASCII as UTF-8 rather than \u escapes
        ensure_ascii=False,
        # Remove unnecessary white space.
        separators=(',', ':'),
        # Sort the keys of dictionaries.
        sort_keys=True,
        # Encode the resulting Unicode as UTF-8 bytes.
    ).encode("UTF-8")


class RawAPI:
    def __init__(self, server_url: str):
        self._session = aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=60))
        self._BASE_URL = server_url
        self._access_token = ''

    async def __make_request(self, http_method: str, method: str, **kwargs) -> Optional[Dict]:
        args = {
            'method':  http_method,
            'url':     f'{self._BASE_URL}/{urllib.parse.quote(method)}',
            'headers': {
                'Authorization': f'Bearer {self._access_token}',
                'Content-Type':  'application/json'
            },
            **kwargs
        }
        if 'data' in args:
            args['data'] = canonical_json_dumps(args['data'])
        if self._access_token == '':
            del args['headers']['Authorization']
        try:
            async with self._session.request(**args) as resp:
                res = await resp.text()
                json_response = json.loads(res)
                if not resp.ok:
                    if 'errcode' in res:
                        raise exceptions.MatrixAPIError.detect(
                            json_response['errcode'], json_response['error'], json_response
                        )
        except asyncio.TimeoutError:
            raise exceptions.MatrixAPINetworkError('Request timeout error')
        except aiohttp.ClientError as e:
            raise exceptions.MatrixAPINetworkError(f"{type(e).__name__}: {e}")
        else:
            return json_response

    @staticmethod
    def _convert_to_model(data: Optional[dict], model: Type[T]) -> Optional[T]:
        try:
            return model(**data)
        except pydantic.ValidationError as e:
            loggers.client.warn(f'validation error {e=} for json {data=}')
            return None

    async def make_request(
            self, http_method: str, method: str, model_type: Optional[Type[T]] = None, **kwargs
    ) -> Optional[Union[List[T], T]]:
        r: Optional[dict] = await self.__make_request(http_method, method, **kwargs)
        if r is not None:
            if model_type is not None:
                if isinstance(r, dict):
                    return self._convert_to_model(r, model_type)
                elif isinstance(r, list) and isinstance(r[0], dict):
                    return [self._convert_to_model(i, model_type) for i in r]
            else:
                return r
        else:
            return None

    def set_access_token(self, access_token: str):
        self._access_token = access_token

    @property
    def is_authorized(self) -> bool:
        return self._access_token != ''
