from aiogram.contrib.middlewares.logging import LoggingMiddleware

from src.config import config

from aiogram import Bot, Dispatcher
from aiogram.types import ParseMode

bot = Bot(config.BOT_API_TOKEN, parse_mode=ParseMode.MARKDOWN_V2)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())