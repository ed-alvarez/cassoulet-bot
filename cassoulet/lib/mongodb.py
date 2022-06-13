from pymongo.database import Database
from pymongo.mongo_client import MongoClient

from lib.config import Config

_config = Config()


def load_mongo_client() -> MongoClient:
    return MongoClient(
        host=_config.MONGO_HOST,
        port=_config.MONGO_PORT,
        username=_config.MONGO_USER,
        password=_config.MONGO_PASS,
        authSource=_config.MONGO_AUTH_SOURCE
    )


def load_db() -> Database:
    client = load_mongo_client()

    return client.get_database(_config.MONGO_DB)
