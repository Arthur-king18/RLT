from aiogram.contrib.middlewares.logging import LoggingMiddleware

from src.config import config

from aiogram import Bot, Dispatcher


bot = Bot(config.BOT_API_TOKEN)
dp = Dispatcher(bot)