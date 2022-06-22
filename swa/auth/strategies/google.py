from sqlalchemy.orm import Session

from . import BaseStrategy
from swa import crud
from swa.core import Config
from swa.schemas import TokenInResponse
from swa.core.utils.auth import generate_tokens, generate_user_id
from swa.schemas import TokenInResponse


class GoogleStrategy(BaseStrategy):
    def authorize(self, db: Session, info: dict):
        user = crud.users.get_by_email(db=db, email=info['email'])
        if user is None:
            user = crud.users.create(
                db=db,
                user_id=generate_user_id(db),
                nick=info['name'],
                email=info['email'],
                coins=Config.START_COINS,
                access_level=0
            )

        tokens = generate_tokens(user_id=user.id, access_level=0)
        crud.auth_tokens.save_token(
            db=db,
            refresh_token=tokens["refresh_token"],
            user_id=user.id,
            access_level=0
        )

        return TokenInResponse(
            user=user,
            expires_in=tokens["expires_in"],
            access_token=tokens["access_token"],
            refresh_token=tokens["refresh_token"],
            user_id=user.id,
            access_level=0
        )