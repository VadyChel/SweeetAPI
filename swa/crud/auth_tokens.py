import typing

from . import BaseCRUD
from sqlalchemy.orm import Session
from swa import crud
from swa.schemas import TokenInDb, TokenInResponse, AuthInRequest, LoginInRequest
from swa.core import Config
from swa.core.utils.response_exception import ResponseException
from swa.core.utils.auth import (
    generate_tokens,
    generate_user_id,
    get_password_hash,
    verify_password,
    validate_refresh_token
)
from swa.models import AuthTokens


class AuthTokensCRUD(BaseCRUD[AuthTokens]):
    def register(self, db: Session, auth: AuthInRequest) -> TokenInResponse:
        crud.auth.check_if_user_registered(db=db, email=auth.email)
        
        user_id = generate_user_id(db)
        password_hash = get_password_hash(auth.password)
        access_level = 0

        crud.auth.create(
            db=db, 
            auth=auth,
            user_id=user_id,
            password_hash=password_hash
        )
        db_user = crud.users.create(
            db=db,
            user_id=user_id,
            nick=auth.nick,
            email=auth.email,
            coins=Config.START_COINS,
            access_level=access_level,
        )

        tokens = generate_tokens(user_id=user_id, access_level=access_level)
        self.save_token(db=db, refresh_token=tokens["refresh_token"], user_id=user_id, access_level=access_level)
        return TokenInResponse(
            **tokens,  # refresh_token, access_token
            user_id=user_id,
            access_level=access_level,
            user=db_user
        )

    def authorize(self, db: Session, auth: LoginInRequest) -> TokenInResponse:
        found_auth = crud.auth.get(db=db, email=auth.email)
        if found_auth is None:
            raise ResponseException(code=10003)

        password_hash = get_password_hash(auth.password)
        is_password_correct = verify_password(plain_password=auth.password, hashed_password=password_hash)
        if not is_password_correct:
            raise ResponseException(code=10009)

        user = crud.users.get(db=db, user_id=found_auth.user_id)
        tokens = generate_tokens(user_id=found_auth.user_id, access_level=user.access_level)
        self.save_token(
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

    def get_token(self, db: Session, user_id: str) -> TokenInDb:
        return db.query(self.model).filter(self.model.user_id == user_id).first()

    def save_token(self, db: Session, refresh_token: str, user_id: str, access_level: int) -> TokenInDb:
        db_token = self.get_token(db=db, user_id=user_id)
        if db_token is not None:
            db.query(self.model).filter(self.model.user_id == user_id).update(
                {"refresh_token": refresh_token, "access_level": access_level}
            )
            db.commit()
            return self.get_token(db=db, user_id=user_id)

        db_token = self.model(
            refresh_token=refresh_token,
            user_id=user_id,
            access_level=access_level
        )
        db.add(db_token)
        db.commit()
        db.refresh(db_token)
        return db_token

    def revoke_token(self, db: Session, refresh_token: str) -> None:
        delete_obj = db.query(self.model).filter(
            self.model.refresh_token == refresh_token
        )
        if delete_obj.first() is None:
            raise HTTPException(status_code=403, detail="Forbidden")

        delete_obj.delete()
        db.commit()

    def get_refresh_token(self, db: Session, refresh_token: str) -> TokenInResponse:
        token_data = validate_refresh_token(refresh_token)
        found_token = db.query(self.model).filter(
            self.model.refresh_token == refresh_token
        ).first()
        if found_token is None or token_data is None:
            raise HTTPException(status_code=401, detail="Unauthorized")

        user = crud.users.get(db=db, user_id=found_token.user_id)
        tokens = generate_tokens(user_id=found_token.user_id, access_level=user.access_level)
        self.save_token(
            db=db,
            refresh_token=tokens["refresh_token"],
            access_level=user.access_level,
            user_id=found_token.user_id
        )

        return TokenInResponse(
            **tokens,  # refresh_token, access_token
            user_id=found_token.user_id,
            access_level=user.access_level,
            user=user
        )


auth_tokens = AuthTokensCRUD(AuthTokens)