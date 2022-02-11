import typing
from fastapi import HTTPException


RESPONSE_CODE_TO_STATUS_CODE = {
    10000: {"status_code": 404, "detail": "User not found"},
    10001: {"status_code": 404, "detail": "Server not found"},
    10002: {"status_code": 404, "detail": "News not found"},
    10003: {"status_code": 400, "detail": "Invalid authorization was provided"},
    10004: {"status_code": 403, "detail": "You don't have permissions"},
    10005: {"status_code": 404, "detail": "Block not found"},
    10006: {"status_code": 403, "detail": "Not enough coins"}
}


class ResponseException(HTTPException):
    def __init__(self, code: int, detail: str = None):
        detail = RESPONSE_CODE_TO_STATUS_CODE[code]["detail"] if detail is None else detail
        super().__init__(
            status_code=RESPONSE_CODE_TO_STATUS_CODE[code]["status_code"],
            detail={"message": detail, "code": code}
        )