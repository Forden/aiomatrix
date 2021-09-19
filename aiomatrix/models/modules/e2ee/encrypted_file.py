from typing import Dict, List

import pydantic


class JWK(pydantic.BaseModel):
    kty: str
    key_ops: List[str]
    alg: str
    k: str
    ext: bool


class EncryptedFile(pydantic.BaseModel):
    url: str
    key: JWK
    iv: str
    hashes: Dict[str, str]
    v: str
