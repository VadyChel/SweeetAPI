import json
import typing
import datetime


class DatetimeSerializer(json.JSONEncoder):
    def default(self, obj: typing.Any) -> typing.Any:
        if isinstance(obj, (datetime.date, datetime.datetime)):
            return obj.timestamp()


def fix_datetime(data: typing.Any) -> typing.Any:
    return json.loads(json.dumps(data, cls=DatetimeSerializer))