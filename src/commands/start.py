from src.config import dp, bot

from aiogram import types, md


@dp.message_handler(commands=["start"])
async def start_handler(message: types.Message):
    firstname = message.from_user.first_name
    lastname = " " + message.from_user.last_name

    text = firstname + lastname if lastname is not None else firstname

    await bot.send_message(message.chat.id, f"Hi, {text}")
