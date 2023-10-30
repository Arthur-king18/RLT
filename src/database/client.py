from src.config import config

from pymongo.mongo_client import MongoClient

client = MongoClient(config.DATABASE_URL)

db = client.test
