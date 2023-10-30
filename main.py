from src.commands import dp
from src.config import config

from aiogram import executor


def main():
    executor.start_polling(dp, skip_updates=config.SKIP_UPDATES)


if __name__ == "__main__":
    main()
