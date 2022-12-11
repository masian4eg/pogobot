import logging

from aiogram import Bot, Dispatcher, executor, types

import tg_messages
from cinema import get_films, num_to_id
from config import KEY_BOT

logging.basicConfig(level=logging.INFO)

bot = Bot(token=KEY_BOT)
dp = Dispatcher(bot)


@dp.message_handler()
async def message_handler(message: types.Message()):
    message_text = message.text
    if message_text == "че по кино":
        await message.answer(f"{tg_messages.films()}")

    if message_text[0] == "/":
        film_num = tg_messages.num_answer(message_text)
        film_id = num_to_id(film_num)
        await message.answer(f"{tg_messages.film(film_id)}", parse_mode="HTML")

    if message_text.lower().startswith("погода "):
        city = message_text.split()
        try:
            await message.answer(f"{tg_messages.weather(city[1])}")
        except Exception:
            await message.answer(f"{tg_messages.weather('Новосибирск')}")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
