import json
import typing
import datetime


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