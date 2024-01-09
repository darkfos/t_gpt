import asyncio
import bot
import logging
import config

from bot.handlers import router
from aiogram import Dispatcher, Bot

import database

async def run_project():
    await database.create_db()

    #Бот
    weather_bot = Bot(token=config.TG_API_KEY)
    dp_w = Dispatcher(bot=weather_bot)
    dp_w.include_router(router=router)

    await dp_w.start_polling(weather_bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(run_project())

