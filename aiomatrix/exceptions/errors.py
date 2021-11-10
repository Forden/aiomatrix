import math
from typing import List, Optional


class AiomatrixError(Exception):
    description_url: Optional[str] = None

    def __init__(self, message: str):
        self.message = message

    def __str__(self):
        message = self.message
        if self.description_url:
            message += f"\n(more info: {self.description_url})"
        return message


class MatrixAPIError(AiomatrixError):
    __suberrors: List['MatrixAPIError'] = []
    error_code = None
    error = None
    raw_data = None

    def __init__(self, error_code: int, error_text: str, raw_data: dict):
        super().__init__(f'{error_code} - {error_text}')
        self.error_code = error_code
        self.error = error_text
        self.raw_data = raw_data

    def __init_subclass__(cls, error_code=None, **kwargs):
        super(MatrixAPIError, cls).__init_subclass__(**kwargs)
        if error_code is not None:
            cls.error_code = error_code.upper()
            # noinspection PyTypeChecker
            cls.__suberrors.append(cls)

    @classmethod
    def detect(cls, error_code: str, error: str, raw_data: dict):
        match = error_code.upper()
        for err in cls.__suberrors:
            if err is cls:
                continue
            if err.error_code == match:
                # noinspection PyCallingNonCallable
                raise err(error_code, error, raw_data)
        raise cls(error_code, error, raw_data)


class MatrixAPINetworkError(MatrixAPIError):
    pass


class MissingToken(MatrixAPIError, error_code='M_MISSING_TOKEN'):
    pass


class UnknownToken(MatrixAPIError, error_code='M_UNKNOWN_TOKEN'):
    pass


class Forbidden(MatrixAPIError, error_code='M_FORBIDDEN'):
    pass


class RoomAliasInUse(MatrixAPIError, error_code='M_ROOM_IN_USE'):
    pass


class Unrecognized(MatrixAPIError, error_code='M_UNRECOGNIZED'):
    pass


class RateLimit(MatrixAPIError, error_code='M_LIMIT_EXCEEDED'):
    description_url = 'https://spec.matrix.org/v1.1/client-server-api/#common-error-codes'

    def __init__(self, error_code: int, error_text: str, raw_data: dict, ):
        super().__init__(error_code, error_text, raw_data)
        self.retry_after_ms = raw_data['retry_after_ms']
        self.retry_after = math.ceil(self.retry_after_ms // 1000)
