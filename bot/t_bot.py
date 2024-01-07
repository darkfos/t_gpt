import asyncio
import logging
import api
import bot.text

from configparser import ConfigParser
from aiogram import Dispatcher, Bot, types, F
from aiogram.filters.command import Command
from aiogram.enums import ParseMode
from aiogram.types import KeyboardButton, InlineKeyboardButton
from .keyboards import kb



logging.basicConfig(level=logging.INFO)

config = ConfigParser()
config.read("config.ini")

weather_bot = Bot(token=config.get("auth", "TG_API_KEY"))

dp_w = Dispatcher(bot=weather_bot)


@dp_w.message(Command("help"))
async def help_command(message: types.Message):
    await message.answer(bot.text[0], parse_mode="HTML")


@dp_w.message(Command("start"))
async def start_command(message: types.Message):
    await message.answer("Выберите ваш <b>город</b>", reply_markup=kb.start_kb, parse_mode="HTML")


@dp_w.message()
async def proccess_callback_button(message: types.Message):
    if message.text in list(api.Weather().get_all_cities().keys()):
        response_to_user: str = f"Вы выбрали город: {message.text}"
        await message.answer(response_to_user)


async def main():
    await dp_w.start_polling(weather_bot)
