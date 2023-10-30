from src.config import dp, bot
from src.filters import IsJsonRequest
from src.utils.aggregation import DataAggregation

import json

from aiogram import types, md


@dp.message_handler(IsJsonRequest())
async def aggregation_handler(message: types.Message):
    await bot.send_message(message.chat.id, await DataAggregation(request=json.loads(message.text)).get_data())
