class Config:
    DB_USER = ''
    DB_HOST = ''
    DB_PASS = ''
    DB_NAME = ''
    DB_PORT = ''

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
    G_RECAPTCHA_SECRET = ""