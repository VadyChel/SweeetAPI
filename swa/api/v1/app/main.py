import typing
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Response
from ratelimit import RateLimitMiddleware, Rule
from ratelimit.backends.redis import RedisBackend
from starlette.types import Scope
from sqlalchemy.exc import SQLAlchemyError
from swa.core import Config
from .routers import users, servers, news, auth, purchases, shop, punishments
from swa.database import engine, Base, SessionLocal
from swa import models


async def auth_func(scope: Scope) -> typing.Tuple[str, str]:
    group = 'default'
    for name, value in scope["headers"]:
        if name == b"X-Forwarded-For":
            ip = value.decode("utf8")
            if ip:
                return ip.split(",")[0], group

    return scope["client"][0], group

Base.metadata.create_all(bind=engine)
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

rate_limit_middleware_backend_options = {
    'host': 'redis-14597.c135.eu-central-1-1.ec2.cloud.redislabs.com',
    'port': 14597,
    'password': "d9hCden7eEqDeez1XHd05Bkt3IziDM9v"
} if Config.DEBUG else {
    'host': 'redis',
    'port': 6379
}

# app.add_middleware(
#     RateLimitMiddleware,
#     authenticate=auth_func,
#     backend=RedisBackend(**rate_limit_middleware_backend_options),
#     config={
#         r"^.*": [Rule(second=150, block_time=3600)],
#     }
# )
app.include_router(
    users.router,
    prefix="/v1"
)
app.include_router(
    servers.router,
    prefix="/v1"
)
app.include_router(
    shop.router,
    prefix="/v1"
)
app.include_router(
    purchases.router,
    prefix="/v1"
)
app.include_router(
    news.router,
    prefix="/v1"
)
app.include_router(
    auth.router,
    prefix="/v1/auth"
)
app.include_router(
    punishments.router,
    prefix="/v1"
)


@app.get("/")
async def index():
    return Response(status_code=204)
