import api
import bot.text
import emoji

from aiogram import types, F
from aiogram.filters.command import Command
from aiogram.types import FSInputFile
from .keyboards import kb, func_about_city_kb, func_neighbors_cities
from .text import weather_1h, about_of_city, neighbors_city
from aiogram import Router

router = Router()


@router.message(Command("help"))
async def help_command(message: types.Message):
    photo: FSInputFile = FSInputFile("bot/img/main_icon.jpg")
    await message.answer_photo(photo=photo, caption=emoji.emojize(bot.text[0] + emoji.emojize(bot.text[1]), language="en"), parse_mode="HTML")


@router.message(Command("start"))
async def start_command(message: types.Message):
    await message.answer("Выберите ваш <b>город</b>", reply_markup=kb.start_kb, parse_mode="HTML")


@router.message(Command("name_city"))
async def about_city_command(message: types.Message):
    message_text: str = "Выберите <b>город</b>"
    keyboard = func_about_city_kb()
    await message.answer(message_text, reply_markup=keyboard.as_markup(), parse_mode="HTML")


@router.message(Command("neighbors"))
async def neighbors_cities(message: types.Message):
    message_text: str = "Выберите интересующий ваc <b>город</b>"
    keyboard_neighbors_cities = func_neighbors_cities()
    await message.answer(message_text, reply_markup=keyboard_neighbors_cities.as_markup(), parse_mode="HTML")


@router.callback_query()
async def callback_response_info_city(callback: types.CallbackQuery):
    if callback.data.endswith("_btn"):
        data_city: tuple | None = api.City(callback.data[:-4]).api_get_info_of_city()
        message_to_user: str = ""
        if data_city:

            for line in range(len(about_of_city)):
                message_to_user += (emoji.emojize(about_of_city[line], language="en") + data_city[line]) + "\n\n"
            await callback.message.answer(message_to_user)

        else:
            await callback.message.answer("Вы исчерпали все попытки за сегодня.")
    else:
        all_city_info: list | None = api.CityNeighbors(callback.data[:-4]).get_neighbors_city()
        message_to_user: str = "Список ближайших городов: \n\n\n"
        if all_city_info:
            for city in range(len(all_city_info)):
                message_to_user += emoji.emojize(neighbors_city + all_city_info[city] + "\n\n", language="en")
            await callback.message.reply(message_to_user)
        else:
            return callback.message.answer("Вы исчерпали все попытки за сегодня.")


@router.message()
async def process_callback_button(message: types.Message):
    all_cities: dict = api.Weather().get_all_cities()
    city_text: str = message.text
    if city_text in all_cities:
        city: str = all_cities.get(message.text)[-1]
        response_to_user: str = f"Вы выбрали город: {message.text}"
        photo = FSInputFile(city)
        await message.answer_photo(photo=photo, caption=response_to_user)

        result_data: str = await weather_data(city_text)
        await message.answer(result_data)

async def weather_data(name_city: str) -> str:
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
            data_weather_for_user += emoji.emojize(all_text_from_1h[line]) + " " + str(city_weather_data[line]) + "\n\n"
        return data_weather_for_user
    else:
        return "К сожалению ваш запрос не удался"
