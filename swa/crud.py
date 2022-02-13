import datetime
import time
import typing
import uuid

from sqlalchemy.orm import Session
from sqlalchemy import desc, func, or_
from fastapi import HTTPException

from swa.core import utils, Config
from . import models, schemas
from .core.utils.auth import generate_user_id, generate_token
from .core.utils.response_exception import ResponseException


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


def get_block_purchases_count(db: Session, block_id: int) -> dict:
    return db.query(
        func.sum(models.UsersPurchases.count).label('count')
    ).filter(models.UsersPurchases.bought_item_id == block_id).first()


def get_user(db: Session, user_id: str) -> schemas.UserInResponse:
    return db.query(models.Users).filter(models.Users.id == user_id).first()


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
    db_auth = models.Auth(
        **{'user_id': user_id, 'password_hash': auth.password, 'nick': auth.nick, 'email': auth.email}
    )
    db.add(db_auth)
    db.commit()
    db.refresh(db_auth)

    db_user = models.Users(
        id=user_id,
        nick=auth.nick,
        email=auth.email,
        coins=Config.START_COINS,
        access_level=0,
        created_at=datetime.datetime.now()
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return authorize(db=db, user_id=user_id)


def authorize(db: Session, user_id: str) -> schemas.TokenInResponse:
    if user_id is None:
        raise ResponseException(code=10008)

    db_token = db.query(models.AuthTokens).filter(models.AuthTokens.user_id == user_id).first()
    if db_token is None:
        password_hash = get_password_hash(db=db, user_id=user_id)
        db_token = models.AuthTokens(
            token=generate_token(user_id=user_id, password_hash=password_hash),
            refresh_token=generate_token(user_id=user_id, password_hash=password_hash),
            user_id=user_id,
            expiry_at=time.time()+1209600
        )
        db.add(db_token)
        db.commit()
        db.refresh(db_token)

    return db_token


def get_token(db: Session, token: str) -> schemas.TokenInResponse:
    return db.query(models.AuthTokens).filter(models.AuthTokens.token == token).first()


def edit_auth(db: Session, user_id: str, updated_fields: dict) -> None:
    db.query(models.Auth).filter(models.Auth.user_id == user_id).update(updated_fields)
    db.commit()


def revoke_token(db: Session, token: str, user_id: str) -> None:
    delete_obj = db.query(models.AuthTokens).filter_by(
        token=token, user_id=user_id
    )
    if delete_obj.first() is None:
        raise HTTPException(status_code=403, detail="Forbidden")

    delete_obj.delete()
    db.commit()


def get_refresh_token(db: Session, refresh_token: str) -> schemas.TokenInResponse:
    update_obj = db.query(models.AuthTokens).filter(
        models.AuthTokens.refresh_token == refresh_token
    )
    found_token = update_obj.first()
    if found_token is None:
        raise HTTPException(status_code=401, detail="Unauthorized")

    password_hash = get_password_hash(db=db, user_id=found_token.user_id)
    payload = {
        'refresh_token': generate_token(user_id=found_token.user_id, password_hash=password_hash),
        'token': generate_token(user_id=found_token.user_id, password_hash=password_hash),
        'expiry_at': time.time()+1209600
    }
    update_obj.update(payload)
    db.commit()
    return get_token(db=db, token=payload['token'])


def get_password_hash(db: Session, user_id: str) -> str:
    db_auth = db.query(models.Auth).filter(models.Auth.user_id == user_id).first()
    if db_auth is not None:
        return db_auth.password_hash


def get_user_id_by_auth(db: Session, auth: schemas.AuthInRequest) -> str:
    found_auth = db.query(models.Auth).filter(
        models.Auth.password_hash == auth.password,
        or_(models.Auth.nick == auth.nick, models.Auth.email == auth.email)
    ).first()

    if found_auth is not None:
        return found_auth.user_id


def get_mutelist(db: Session, skip: int = 0, limit: int = 20) -> typing.List[schemas.Punishment]:
    return (db.query(models.Punishments).filter(models.Punishments.type == 'mute')
            .offset(skip).limit(limit).all())


def get_banlist(db: Session, skip: int = 0, limit: int = 20) -> typing.List[schemas.Punishment]:
    return (db.query(models.Punishments).filter(models.Punishments.type == 'ban')
            .offset(skip).limit(limit).all())


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


def get_server_stats(db: Session, server_id: int) -> schemas.ServerStats:
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