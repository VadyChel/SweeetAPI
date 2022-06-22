import json
import typing
import datetime

from pydantic import BaseModel
from fastapi.responses import JSONResponse


class DatetimeSerializer(json.JSONEncoder):
    def default(self, obj: typing.Any) -> typing.Any:
        if isinstance(obj, (datetime.date, datetime.datetime)):
            return obj.isoformat()


def fix_datetime(data: typing.Any) -> typing.Any:
    return json.loads(json.dumps(data, cls=DatetimeSerializer))


def model_to_dict(row):
    if row is None:
        return None

    d = {}
    for column in row.__table__.columns:
        d[column.name] = getattr(row, column.name)

    return d


def create_auth_response(auth_schema: BaseModel) -> JSONResponse:
    fixed_content = fix_datetime(auth_schema.dict())
    response = JSONResponse(content=fixed_content)
    response.set_cookie(
        key="refresh_token",
        value=fixed_content["refresh_token"],
        expires=fixed_content["expires_in"],
        httponly=True
    )
    return response
