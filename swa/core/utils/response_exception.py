import typing
from fastapi import HTTPException


RESPONSE_CODE_TO_STATUS_CODE = {
    10000: 404,
    10001: 404,
    10002: 404,
    10003: 400,
    10004: 400,
    10005: 400,
    10006: 403,
    10007: 400,
    10008: 404,
    10009: 400,
    10010: 404,
    10011: 404,
    10012: 404,
    10013: 400,
    10014: 400,
    10015: 404,
    10016: 401,
    10017: 403,
    10018: 400,
    10019: 400,
    10020: 400,
    10021: 400,
    10022: 400,
    10023: 400,
    10024: 400,
    10025: 400,
    10026: 404
}


class ResponseException(HTTPException):
    def __init__(self, code: int, detail: typing.Any):
        super().__init__(
            status_code=RESPONSE_CODE_TO_STATUS_CODE[code],
            detail={"message": detail, "code": code}
        )