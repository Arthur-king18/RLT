import os

from typing import List
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

BOT_API_TOKEN = os.environ.get("BOT_API_TOKEN")
DATABASE_URL = os.environ.get("DATABASE_URL")


class Config(BaseModel):
    SKIP_UPDATES: bool = True
    BOT_API_TOKEN: str = BOT_API_TOKEN
    DATABASE_URL: str = DATABASE_URL


config = Config()
