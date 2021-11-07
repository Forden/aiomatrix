import datetime

from pydantic import BaseModel, Extra, root_validator

from ...utils.mixins import ContextVarMixin


class MatrixObject(BaseModel, ContextVarMixin):
    raw: dict

    class Config:
        allow_mutation = True
        json_encoders = {datetime.datetime: lambda dt: int(dt.timestamp())}
        validate_assignment = True
        extra = Extra.ignore

    @root_validator(pre=True)
    def _parse_raw(cls, values: dict):
        values['raw'] = values.copy()
        return values
