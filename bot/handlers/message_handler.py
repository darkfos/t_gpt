import api
import emoji
import random

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile

from bot import FormAdmin, get_admin_bt, FormReview
from database.services import admin_service, review_service
from bot.text import weather_1h
from api import ForecastWeather5d

admin_router = Router()


@admin_router.message(FormAdmin.password)
async def password_admin(message: Message, state=FSMContext):
    password_admin: str = message.text
    response_to_admin_table = (await admin_service.get_one_admin(int(message.from_user.id)))[0][-1]
    if response_to_admin_table.password == password_admin:
        await message.answer(emoji.emojize(":check_mark_button: Успешно. Добро пожаловать в админ панель %s" % message.from_user.full_name), language="en")
        await state.set_state(FormAdmin.sel_option)
        await message.answer(emoji.emojize(":scroll: Выберите пункт <b>меню</b> %s" % message.from_user.full_name, language="en"), reply_markup=get_admin_bt(), parse_mode="HTML")
    else:
        await message.answer(":cross_mark: Пароль <u>неверен</u>", language="en", parse_mode="HTML")


@admin_router.message(FormReview.name)
async def name_user(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(FormReview.age)
    await message.answer(emoji.emojize(":check_mark_button: Введите свой возраст"), language="en")


@admin_router.message(FormReview.age)
async def age_user(message: Message, state: FSMContext):
    if message.text.isdigit():
        await state.update_data(age=int(message.text))
        await state.set_state(FormReview.review_text)
        await message.answer(emoji.emojize(":check_mark_button: Замечательно, теперь напишите свой отзыв"), language="en")
    else:
        await message.answer(emoji.emojize(":cross_mark: Неверно был введён возраст"), language="en")


@admin_router.message(FormReview.review_text)
async def review_text_from_user(message: Message, state: FSMContext):
    if await state.update_data(review_text=message.text):
        state_data = await state.get_data()
        await state.clear()
        data_for_user: list = [state_data.get(key) for key in state_data.keys()]
        data_for_user.insert(0, message.from_user.id)
        review_obj: tuple = data_for_user[0], data_for_user[2], data_for_user[1], data_for_user[-1]
        result = await review_service.get_one_reviews(data_for_user[0])
        if len(result) == 0:
            await review_service.add_one_reviews(*review_obj)
            await message.answer(emoji.emojize(":check_mark_button: Успешно! Спасибо за ваш отзыв."), language="en")
            await message.answer(emoji.emojize(f":check_mark_button: {message.from_user.full_name} ваш отзыв был успешно отправлен!"), language="en")
        else:
            await message.answer(f"<b>{message.from_user.full_name}</b> к сожалению вы уже отправляли свой отзыв", parse_mode="HTML")
    else:
        await message.answer(emoji.emojize(":cross_mark: Ошибка, попробуйте ещё раз"), language="en")


@admin_router.message(FormAdmin.sel_option)
async def sel_option_admin(message: Message, state=FSMContext):
    all_cities: dict = api.Weather().get_all_cities()
    city_text: str = message.text
    all_record_review = await review_service.get_all_reviews()
    match message.text:
        case "Удалить отзыв":
            await message.answer(emoji.emojize(":bell: Вы выбрали пункт меню - <b>удалить</b>\nПожалуйста введите id отзыва, который хотите удалить"), language="en", parse_mode="HTML")
            await state.set_state(FormAdmin.sel_point)
        case "Узнать количество отзывов":
            await message.answer(emoji.emojize(":bell: Вы выбрали пункт меню - <b>количество отзывов</b>"), language="en", parse_mode="HTML")
            await message.answer("<b>Ждите.</b> Операция выполняется", parse_mode="HTML")
            await message.answer(f"<b>Количество отзывов:</b> {len(all_record_review)}", parse_mode="HTML")
        case "Уникальный отзыв":
            await message.answer(emoji.emojize(":bell: Вы выбрали пункт меню - <b>уникальный отзыв</b>"), language="en", parse_mode="HTML")
            await message.answer("<b>Ждите.</b> Операция выполняется", parse_mode="HTML")
            random_review = random.choice(all_record_review)
            await message.answer(
                f"<b>Имя:</b> {random_review.name}\n<b>Возраст:</b> {random_review.age}\n<b>Текст:</b> {random_review.review_text}\n<b>ID</b>: {random_review.id}\n<b>ID_telegram</b>: {random_review.tg_id}", parse_mode="HTML"
            )


@admin_router.message(FormAdmin.sel_point)
async def sel_point(message: Message, state=FSMContext):
    unique_record_review = await review_service.get_one_review_id(int(message.text))
    if unique_record_review:
        try:
            await review_service.del_one_reviews(int(message.text))
            await message.reply(emoji.emojize(":bell: Запись была удалена."))
        except Exception:
            await message.reply("Внутренняя ошибка, неудалось удалить запись.")
    else:
        await message.reply("Такой записи нет.")


@admin_router.message()
async def process_callback_button(message: Message):
    all_cities: dict = api.Weather().get_all_cities()
    city_text: str = message.text
    if city_text[2:] in all_cities and city_text[0] == emoji.emojize(":sunset:", language="en"):
        city: str = all_cities.get(message.text[2:])[-1]
        response_to_user: str = emoji.emojize(f":bell: Вы выбрали город: <b>{message.text[2:]}</b>", language="en")
        photo = FSInputFile(city)
        await message.answer_photo(photo=photo, caption=response_to_user,  parse_mode="HTML")

        result_data: str = await weather_data(city_text[2:])
        await message.answer(result_data)
    elif city_text[0] == emoji.emojize(":night_with_stars:", language="en") and city_text[2:] in all_cities:
        weather_to_5d: list = ForecastWeather5d(city_text[2:]).get_info_to_weather_5d()
        print("23", weather_to_5d, "234")
        id_day = 1
        days_name = ["Сегодня", "Завтра", "Послезавтра"]
        for message_weather in weather_to_5d:
            await message.answer(
                text=emoji.emojize(f":bell: День:   <b>{days_name[id_day-1] if id_day-1 < len(days_name) else id_day}</b>", language="en") + \
                    f"\n📅  <b>Дата</b>: {message_weather.get("Date")}" \
                    f"\n🌡   <b>Температура</b> (мин): {round(message_weather.get("Temperature")[0], 2)}" \
                    f"\n🌡   <b>Температура</b> (макс): {round(message_weather.get("Temperature")[-1], 2)}" \
                    f"\n☀   <b>День</b>: {message_weather.get("Day")}" \
                    f"\n🌑  <b>Ночь</b>: {message_weather.get("Night")}",
                parse_mode="HTML"
            )
            id_day += 1



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
        return emoji.emojize(":cross_mark: К сожалению ваш запрос не удался", language="HTML")