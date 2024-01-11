from api import Weather

from aiogram.types import KeyboardButton, InlineKeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

start_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=city_name) for city_name in list(Weather().get_all_cities().keys())
        ]
    ],
    resize_keyboard=True,
    input_field_placeholder="Локация",
    one_time_keyboard=True
)


def func_about_city_kb():
    about_city_kb = InlineKeyboardBuilder()

    for city_name in list(Weather().get_all_cities().keys()):
        about_city_kb.row(InlineKeyboardButton(text=city_name, callback_data=city_name+"_btn"))

    return about_city_kb


def func_neighbors_cities():
    all_cities: InlineKeyboardBuilder = InlineKeyboardBuilder()

    for city_name in list(Weather().get_all_cities().keys()):
        all_cities.row(InlineKeyboardButton(text=city_name, callback_data=city_name+"_inb"))

    return all_cities


def review_text_butt():
    button_response: InlineKeyboardBuilder = InlineKeyboardBuilder()
    button_response.row(InlineKeyboardButton(text="Да", callback_data="Yes_nbt"))
    button_response.row(InlineKeyboardButton(text="Нет", callback_data="No_nbt"))

    return button_response