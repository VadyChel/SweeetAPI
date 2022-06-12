class Config:
    DB_USER = 'postgres'
    DB_HOST = '127.0.0.1'
    DB_PASS = 'zyzel19'
    DB_NAME = 'sweeet'
    DB_PORT = '5400'

    START_BLOKSY = 500
    START_COINS = 10
    COINS_EXCHANGE_FUNC = lambda coins: coins * 100

    NICK_MIN_LENGTH = 3
    NICK_MAX_LENGTH = 48
    PASSWORD_MIN_LENGTH = 10

    JWT_REFRESH_SECRET = ''
    JWT_ACCESS_SECRET = ''

    DEBUG = True

    CLIENT_URL = 'http://localhost:3000'