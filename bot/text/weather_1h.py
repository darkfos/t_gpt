import api


from aiogram.enums import ParseMode
all_cities = ""
for city in list(api.Weather().get_all_cities()):
    all_cities += f":cityscape_at_dusk: <u>{city}</u>\n"

text = [
    "<b>Привет!</b> Я бот Стивен и я помогу тебе узнать текущую погоду.\n\nНа выбор имеется" + \
    " <b>3 города: </b>" + "\n"*2 + all_cities,
    "\nА вот и мой перечень команд: \n\n\n" + ":star:   /start - Запуск бота, позволяет узнать прогноз погоды о городе\n" + \
    "\n:star:   /help - Вывод документации использования\n" + "\n:star:   /name_city - Вывод информации об указанном городе"
]

weather_data = [
    "🌡️  Температура сейчас: ",
    "🌦️ Погодное состояние: ",
    "🕓 Время: ",
    "🌓 Время суток: "
]