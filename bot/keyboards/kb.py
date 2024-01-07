from api import Weather

from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

start_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=i) for i in list(Weather().get_all_cities().keys())
        ]
    ],
    resize_keyboard=True,
    input_field_placeholder="Локация",
    one_time_keyboard=True
)