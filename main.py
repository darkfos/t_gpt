import asyncio
import logging
import config

from bot.handlers import router
from bot.handlers.callback_handler import fsm_router
from bot.handlers import admin_router
from aiogram import Dispatcher, Bot
from aiogram.fsm.storage.memory import MemoryStorage
from database import create_db, admin_service



async def run_project():
    await create_db()

    # Бот
    weather_bot = Bot(token=config.TG_API_KEY)
    storage = MemoryStorage()
    dp_w = Dispatcher(bot=weather_bot, storage=storage)
    dp_w.include_routers(
        router,
        admin_router,
        fsm_router
    )
    await dp_w.start_polling(weather_bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(run_project())
