from src.config import dp, bot

from aiogram import types


@dp.message_handler()
async def not_valid_request_handler(message: types.Message):
    await bot.send_message(message.chat.id, 'Невалидный запос. Пример запроса: {"dt_from": "2022-09-01T00:00:00",'
                                            ' "dt_upto": "2022-12-31T23:59:00", "group_type": "month"}')
