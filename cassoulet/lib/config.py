from os import environ
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv(), verbose=True)


class Config:
    MONGO_HOST: str = environ.get('MONGO_HOST') or 'localhost'
    MONGO_PORT: int = environ.get('MONGO_PORT') or 27017
    MONGO_USER: str = environ.get('MONGO_USER') or 'root'
    MONGO_PASS: str = environ.get('MONGO_PASS') or 'root'
    MONGO_DB: str = environ.get('MONGO_DB') or 'cassoulet'
    MONGO_AUTH_SOURCE = environ.get('MONGO_AUTH_SOURCE') or 'admin'

    DISCORD_TOKEN: str = environ.get('DISCORD_TOKEN') or ''
