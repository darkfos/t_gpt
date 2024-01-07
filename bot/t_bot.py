import asyncio
import logging
import api
import bot.text

from configparser import ConfigParser
from aiogram import Dispatcher, Bot, types, F
from aiogram.filters.command import Command
from aiogram.enums import ParseMode
from aiogram.types import KeyboardButton, InlineKeyboardButton, FSInputFile
from .keyboards import kb



logging.basicConfig(level=logging.INFO)

config = ConfigParser()
config.read("config.ini")

weather_bot = Bot(token=config.get("auth", "TG_API_KEY"))

dp_w = Dispatcher(bot=weather_bot)


@dp_w.message(Command("help"))
async def help_command(message: types.Message):
    photo: FSInputFile = FSInputFile("bot/img/free-icon-weather-831268.png")
    await message.answer_photo(photo=photo, caption=bot.text[0], parse_mode="HTML")


@dp_w.message(Command("start"))
async def start_command(message: types.Message):
    await message.answer("Выберите ваш <b>город</b>", reply_markup=kb.start_kb, parse_mode="HTML")


@dp_w.message()
async def proccess_callback_button(message: types.Message):
    all_cities: dict = api.Weather().get_all_cities()
    if message.text in all_cities:
        city: str = all_cities.get(message.text)[-1]
        response_to_user: str = f"Вы выбрали город: {message.text}"
        photo = FSInputFile(city)
        await message.answer_photo(photo=photo, caption=response_to_user)

async def main():
    await dp_w.start_polling(weather_bot)
