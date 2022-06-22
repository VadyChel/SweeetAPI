from sqlalchemy.orm import Session

from . import LocalStrategy
from swa.core.utils.response_exception import ResponseException
from swa.schemas import TokenInResponse, AuthInRequest, LoginInRequest
from swa import crud
from swa.core import Config
from swa.core.utils.auth import (
    generate_tokens,
    generate_user_id,
    get_password_hash,
    verify_password
)


class DefaultStrategy(LocalStrategy):
    def register(self, db: Session, info: AuthInRequest) -> TokenInResponse:
        crud.auth.check_if_user_registered(db=db, email=info.email)

        user_id = generate_user_id(db)
        password_hash = get_password_hash(info.password)
        access_level = 0

        crud.auth.create(
            db=db,
            auth=info,
            user_id=user_id,
            password_hash=password_hash
        )
        db_user = crud.users.create(
            db=db,
            user_id=user_id,
            nick=info.nick,
            email=info.email,
            coins=Config.START_COINS,
            access_level=access_level,
        )

        tokens = generate_tokens(user_id=user_id, access_level=access_level)
        crud.auth_tokens.save_token(
            db=db,
            refresh_token=tokens["refresh_token"],
            user_id=user_id,
            access_level=access_level
        )
        return TokenInResponse(
            **tokens,  # refresh_token, access_token
            user_id=user_id,
            access_level=access_level,
            user=db_user
        )

    def authorize(self, db: Session, info: LoginInRequest) -> TokenInResponse:
        found_auth = crud.auth.get(db=db, email=info.email)
        if found_auth is None:
            raise ResponseException(code=10003)

        password_hash = get_password_hash(info.password)
        is_password_correct = verify_password(
            plain_password=info.password,
            hashed_password=password_hash
        )
        if not is_password_correct:
            raise ResponseException(code=10009)

        user = crud.users.get(db=db, user_id=found_auth.user_id)
        tokens = generate_tokens(user_id=found_auth.user_id, access_level=user.access_level)
        crud.auth_tokens.save_token(
            db=db,
            refresh_token=tokens["refresh_token"],
            user_id=found_auth.user_id,
            access_level=user.access_level
        )

        return TokenInResponse(
            **tokens,  # refresh_token, access_token
            user_id=found_auth.user_id,
            access_level=user.access_level,
            user=user
        )