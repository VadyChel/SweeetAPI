import datetime
import time
import typing
import uuid

from sqlalchemy.orm import Session
from sqlalchemy import desc, func, or_
from fastapi import HTTPException

from swa.core import Config
from . import models, schemas
from .core.utils.auth import (
    generate_tokens,
    generate_user_id,
    get_password_hash,
    verify_password,
    validate_refresh_token
)
from .core.utils.response_exception import ResponseException
from .core.utils.other import model_to_dict


def get_server(db: Session, server_id: int) -> schemas.ServerInResponse:
    return db.query(models.Servers).filter(models.Servers.id == server_id).first()


def get_servers(db: Session, skip: int = 0, limit: int = 20) -> typing.List[schemas.ServerInResponse]:
    return db.query(models.Servers).offset(skip).limit(limit).all()


def get_news(db: Session, news_id: int) -> schemas.NewsInResponse:
    return db.query(models.News).filter(models.News.id == news_id).first()


def get_all_news(db: Session, skip: int = 0, limit: int = 20) -> typing.List[schemas.NewsInResponse]:
    return db.query(models.News).offset(skip).limit(limit).all()


def add_news(db: Session, news: schemas.NewsInRequest):
    db_news = models.News(**news.dict())
    db.add(db_news)
    db.commit()
    db.refresh(db_news)
    return db_news


def edit_news(
        db: Session,
        news_id: int,
        news: schemas.NewsInRequestEdit
):
    db.query(models.News).filter(models.News.id == news_id).update(news.dict(exclude_none=True))
    db.commit()
    return get_news(db=db, news_id=news_id)


def delete_news(db: Session, news_id: int):
    deleted_news = get_news(db=db, news_id=news_id)
    db.query(models.News).filter(models.News.id == news_id).delete()
    db.commit()
    return deleted_news


def get_user_purchases(
        db: Session, user_id: str, skip: int = 0, limit: int = 20
) -> typing.List[schemas.UserPurchaseInResponse]:
    return (db.query(models.UsersPurchases)
            .filter(models.UsersPurchases.user_id == user_id)
            .offset(skip)
            .limit(limit)
            .all())


def get_all_purchases(
        db: Session, skip: int = 0, limit: int = 20
) -> typing.List[schemas.UserPurchaseInResponse]:
    return (db.query(models.UsersPurchases)
            .offset(skip)
            .limit(limit)
            .all())


def get_user_purchases_count(db: Session, user_id: str) -> int:
    return db.query(models.UsersPurchases).filter(models.UsersPurchases.user_id == user_id).count()


def get_block_purchases_count(db: Session, block_id: int) -> int:
    return db.query(func.count(models.UsersPurchases.id)).filter(
        models.UsersPurchases.bought_item_id == block_id
    ).first()[0]


def get_user(db: Session, user_id: str) -> schemas.UserInResponse:
    found_user = db.query(models.Users).filter(models.Users.id == user_id).first()
    if found_user is None:
        raise ResponseException(code=10000)

    return found_user


def edit_user(
        db: Session,
        user_id: str,
        updated_fields: dict
):
    db.query(models.Users).filter(models.Users.id == user_id).update(updated_fields)
    db.commit()
    return get_user(db=db, user_id=user_id)


def get_current_user_id(db: Session, token: str) -> str:
    found_token = db.query(models.AuthTokens).filter(models.AuthTokens.token == token).first()
    if found_token is not None:
        return found_token.user_id


def get_shop(db: Session, skip: int = 0, limit: int = 20) -> typing.List[schemas.ShopItemInResponse]:
    return db.query(models.Shop).offset(skip).limit(limit).all()


def get_shop_item(db: Session, block_id: id) -> schemas.ShopItemInResponse:
    return db.query(models.Shop).filter(models.Shop.id == block_id).first()


def register(db: Session, auth: schemas.AuthInRequest) -> schemas.TokenInResponse:
    if db.query(models.Auth).filter(models.Auth.email == auth.email).first() is not None:
        raise ResponseException(code=10007)

    user_id = generate_user_id(db)
    password_hash = get_password_hash(auth.password)
    access_level = 0
    db_auth = models.Auth(
        user_id=user_id,
        password_hash=password_hash,
        nick=auth.nick,
        email=auth.email
    )
    db.add(db_auth)
    db.commit()
    db.refresh(db_auth)

    db_user = models.Users(
        id=user_id,
        nick=auth.nick,
        email=auth.email,
        coins=Config.START_COINS,
        access_level=access_level,
        created_at=datetime.datetime.now()
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    tokens = generate_tokens(user_id=user_id, access_level=access_level)
    save_token(db=db, refresh_token=tokens["refresh_token"], user_id=user_id, access_level=access_level)
    return schemas.TokenInResponse(
        **tokens,  # refresh_token, access_token
        user_id=user_id,
        access_level=access_level,
        user=db_user
    )


def authorize(db: Session, auth: schemas.LoginInRequest) -> schemas.TokenInResponse:
    found_auth = db.query(models.Auth).filter(models.Auth.email == auth.email).first()
    if found_auth is None:
        raise ResponseException(code=10008)

    password_hash = get_password_hash(auth.password)
    is_password_correct = verify_password(plain_password=auth.password, hashed_password=password_hash)
    if not is_password_correct:
        raise ResponseException(code=10009)

    user = get_user(db=db, user_id=found_auth.user_id)
    tokens = generate_tokens(user_id=found_auth.user_id, access_level=user.access_level)
    save_token(
        db=db,
        refresh_token=tokens["refresh_token"],
        user_id=found_auth.user_id,
        access_level=user.access_level
    )

    return schemas.TokenInResponse(
        **tokens,  # refresh_token, access_token
        user_id=found_auth.user_id,
        access_level=user.access_level,
        user=user
    )


def get_token(db: Session, user_id: str) -> schemas.TokenInDb:
    return db.query(models.AuthTokens).filter(models.AuthTokens.user_id == user_id).first()


def save_token(db: Session, refresh_token: str, user_id: str, access_level: int) -> schemas.TokenInDb:
    db_token = get_token(db=db, user_id=user_id)
    if db_token is not None:
        db.query(models.AuthTokens).filter(models.AuthTokens.user_id == user_id).update(
            {"refresh_token": refresh_token, "access_level": access_level}
        )
        db.commit()
        return get_token(db=db, user_id=user_id)

    db_token = models.AuthTokens(
        refresh_token=refresh_token,
        user_id=user_id,
        access_level=access_level
    )
    db.add(db_token)
    db.commit()
    db.refresh(db_token)
    return db_token


def edit_auth(db: Session, user_id: str, updated_fields: dict) -> None:
    db.query(models.Auth).filter(models.Auth.user_id == user_id).update(updated_fields)
    db.commit()


def revoke_token(db: Session, refresh_token: str) -> None:
    delete_obj = db.query(models.AuthTokens).filter(
        models.AuthTokens.refresh_token == refresh_token
    )
    if delete_obj.first() is None:
        raise HTTPException(status_code=403, detail="Forbidden")

    delete_obj.delete()
    db.commit()


def get_refresh_token(db: Session, refresh_token: str) -> schemas.TokenInResponse:
    token_data = validate_refresh_token(refresh_token)
    found_token = db.query(models.AuthTokens).filter(
        models.AuthTokens.refresh_token == refresh_token
    ).first()
    if found_token is None or token_data is None:
        raise HTTPException(status_code=401, detail="Unauthorized")

    user = get_user(db=db, user_id=found_token.user_id)
    tokens = generate_tokens(user_id=found_token.user_id, access_level=user.access_level)
    save_token(
        db=db,
        refresh_token=tokens["refresh_token"],
        access_level=user.access_level,
        user_id=found_token.user_id
    )

    return schemas.TokenInResponse(
        **tokens,  # refresh_token, access_token
        user_id=found_token.user_id,
        access_level=user.access_level,
        user=user
    )


def get_mutelist(db: Session, skip: int = 0, limit: int = 20) -> typing.List[schemas.Punishment]:
    return (db.query(models.Punishments).filter(models.Punishments.type == 'mute')
            .offset(skip).limit(limit).all())


def get_banlist(db: Session, skip: int = 0, limit: int = 20) -> typing.List[schemas.Punishment]:
    return (db.query(models.Punishments).filter(models.Punishments.type == 'ban')
            .offset(skip).limit(limit).all())


def get_user_punishments(
        db: Session, user_id: str, skip: int = 0, limit: int = 20
) -> typing.List[schemas.Punishment]:
    return (db.query(models.Punishments).filter(models.Punishments.user_id == user_id)
            .offset(skip).limit(limit).all())


def get_user_bought_items(db: Session, user_id: str) -> typing.List[schemas.BoughtItemInResponse]:
    return db.query(models.BoughtItems).filter(models.BoughtItems.user_id == user_id).all()


def add_user_bought_items(db: Session, block: schemas.BoughtItemInRequest):
    db_item = models.BoughtItems(**block.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def add_user_purchase(db: Session, purchase: schemas.UserPurchaseInRequest):
    db_purchase = models.UsersPurchases(**purchase.dict())
    db.add(db_purchase)
    db.commit()
    db.refresh(db_purchase)
    return db_purchase


def get_user_balance(db: Session, user_id: str) -> typing.List[schemas.BloksyBalance]:
    return db.query(models.BloksyBalance).filter(models.BloksyBalance.user_id == user_id).all()


def get_user_balance_on_server(db: Session, user_id: str, server_id: int) -> schemas.BloksyBalance:
    return db.query(models.BloksyBalance).filter(
        models.BloksyBalance.user_id == user_id,
        models.BloksyBalance.server_id == server_id
    ).first()


def get_server_stats(db: Session, server_id: int) -> typing.Optional[schemas.ServerStats]:
    db_stats = (
        db.query(models.ServersStat)
        .filter(models.ServersStat.server_id == server_id)
        .order_by(desc(models.ServersStat.time))
        .first()
    )
    if db_stats is None:
        return

    record_online = (
        db.query(models.ServersStat)
        .filter(models.ServersStat.server_id == server_id)
        .order_by(desc(models.ServersStat.online))
        .first()
    )
    return schemas.ServerStats(**db_stats.__dict__, record_online=record_online.online)


def get_bloksy_balances_top_on_server(db: Session, server_id: int) -> typing.List[schemas.BloksyBalance]:
    return (
        db.query(models.BloksyBalance)
        .filter(models.BloksyBalance.server_id == server_id)
        .order_by(desc(models.BloksyBalance.bloksy)).limit(100).all()
    )


def change_bloksy_balance(
        db: Session, server_id: int, user_id: str, added_bloksy: int
) -> None:
    balance_query = db.query(models.BloksyBalance).filter(
        models.BloksyBalance.server_id == server_id,
        models.BloksyBalance.user_id == user_id
    )
    old_balance = balance_query.first()
    if old_balance is None:
        add_bloksy_balance(db=db, user_id=user_id, server_id=server_id, bloksy=added_bloksy)
    else:
        balance_query.update({'bloksy': old_balance.bloksy + added_bloksy})
        db.commit()


def add_bloksy_balance(
        db: Session, user_id: str, server_id: int, bloksy: int = 0
) -> schemas.BloksyBalance:
    db_bloksy = models.BloksyBalance(user_id=user_id, server_id=server_id, bloksy=bloksy)
    db.add(db_bloksy)
    db.commit()
    db.refresh(db_bloksy)
    return db_bloksy
