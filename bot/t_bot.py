import asyncio
import logging
import api
import bot.text
import config

from aiogram import Dispatcher, Bot, types, F
from aiogram.filters.command import Command
from aiogram.enums import ParseMode
from aiogram.types import KeyboardButton, InlineKeyboardButton, FSInputFile
from .keyboards import kb
from .text import weather_1h


logging.basicConfig(level=logging.INFO)
weather_bot = Bot(token=config.TG_API_KEY)

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

        await weather_data(message.text, message.chat.id)

async def weather_data(name_city: str, chat_id: int):
    """
    Обрабатывает данные о погоде, вывод
    :return:
    """
    forecast_weather: api.Weather = api.Weather()
    city_weather_data: tuple = forecast_weather.get_city(name_city)

    if city_weather_data:
        data_weather_for_user: str = ""
        all_text_from_1h: list = weather_1h.weather_data
        for line in range(len(all_text_from_1h)):
            data_weather_for_user += all_text_from_1h[line] + " " + city_weather_data[line]
        await weather_bot.send_message(chat_id=chat_id, text=data_weather_for_user)
    else:
        await weather_bot.send_message(chat_id=chat_id, text="К сожалению ваш запрос не удался")


async def main():
    await dp_w.start_polling(weather_bot)
