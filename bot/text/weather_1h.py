import api


from aiogram.enums import ParseMode
all_cities = ""
for city in list(api.Weather().get_all_cities()):
    all_cities += f"<u>{city}</u>\n"

text = [
    "Привет! Я бот, который поможет тебе узнать текущую погоду.\n\nНа выбор имеется" + \
    " 3 города: " + "\n"*2 + all_cities
]