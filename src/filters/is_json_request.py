from aiogram import types
from aiogram.dispatcher.filters import Filter


class IsJsonRequest(Filter):
    async def check(self, message: types.Message) -> bool:
        return message.text.startswith("{") and message.text.endswith("}")
