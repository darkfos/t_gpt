from aiogram.utils.keyboard import KeyboardButton, ReplyKeyboardMarkup

__admin_option = ["Удалить отзыв", "Узнать количество отзывов", "Уникальный отзыв"]

def get_admin_bt():
    sel_admin_menu = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=text) for text in __admin_option
            ]
        ],
        resize_keyboard=True,
        input_field_placeholder="Локация",
        one_time_keyboard=True
    )
    return sel_admin_menu


def get_option():
    return __admin_option