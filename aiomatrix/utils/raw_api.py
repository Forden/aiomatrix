import json
from typing import Dict, Optional

import aiohttp

from . import exceptions


class RawAPI:
    def __init__(self, server_url: str):
        self._session = aiohttp.ClientSession()
        self._BASE_URL = server_url
        self._access_token = ''

    async def __make_request(self, http_method: str, method: str, **kwargs) -> Optional[Dict]:
        args = {
            'method':  http_method,
            'url':     f'{self._BASE_URL}/{method}',
            'headers': {
                'Authorization': f'Bearer {self._access_token}',
                'Content-Type':  'application/json'
            },
            **kwargs
        }
        if 'data' in args:
            args['data'] = json.dumps(args['data'])
        if self._access_token == '':
            del args['headers']['Authorization']
        async with self._session.request(**args) as resp:
            res = await resp.json()
            if not resp.ok:
                if 'errcode' in res:
                    raise exceptions.MatrixAPIError.detect(res['errcode'], res['error'], res)
                    # return errors.parse_error(res)
            return await resp.json()

    async def make_request(self, http_method: str, method: str, model_type=None, **kwargs):
        r = await self.__make_request(http_method, method, **kwargs)
        if isinstance(r, dict):
            print(r)
            return model_type(**r)
        else:
            return r

    def set_access_token(self, access_token: str):
        self._access_token = access_token
