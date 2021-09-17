from typing import List


class MatrixAPIError(Exception):
    __suberrors: List['MatrixAPIError'] = []
    error_code = None
    error = None
    raw_data = None

    def __init_subclass__(cls, error_code=None, **kwargs):
        super(MatrixAPIError, cls).__init_subclass__(**kwargs)
        if error_code is not None:
            cls.error_code = error_code.upper()
            cls.__suberrors.append(cls)

    @classmethod
    def detect(cls, error_code: str, error: str, raw_data: dict):
        match = error_code.upper()
        for err in cls.__suberrors:
            if err is cls:
                continue
            if err.error_code == match:
                raise err(error_code, error, raw_data)
        raise cls(error_code, error, raw_data)


class Forbidden(MatrixAPIError, error_code='M_FORBIDDEN'):
    pass
