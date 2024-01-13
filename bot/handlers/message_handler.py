import api
import emoji

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile

from bot import FormAdmin, get_admin_bt, FormReview
from database.services import admin_service, review_service
from bot.text import weather_1h


admin_router = Router()


@admin_router.message(FormAdmin.password)
async def password_admin(message: Message, state=FSMContext):
    password_admin: str = message.text
    response_to_admin_table = (await admin_service.get_one_admin(int(message.from_user.id)))[0][-1]
    if response_to_admin_table.password == password_admin:
        await message.answer(emoji.emojize(":check_mark_button: Успешно. Добро пожаловать в админ панель %s" % message.from_user.full_name), language="en")
        await state.set_state(FormAdmin.sel_option)
        await message.answer(emoji.emojize(":scroll: Выберите пункт <b>меню</b> %s" % message.from_user.full_name, reply_markup=get_admin_bt()), language="en", parse_mode="HTML")
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
        await message.answer(emoji.emojize(":check_mark_button: Успешно! Спасибо за ваш отзыв."), language="en")
        state_data = await state.get_data()
        await state.clear()
        data_for_user: list = [state_data.get(key) for key in state_data.keys()]
        data_for_user.insert(0, message.from_user.id)
        review_obj: tuple = data_for_user[0], data_for_user[-1], data_for_user[1], data_for_user[2]
        result = await review_service.get_one_reviews(data_for_user[0])
        if len(result) == 0:
            await review_service.add_one_reviews(*review_obj)
            await message.answer(emoji.emojize(f":check_mark_button: {message.from_user.full_name} ваш отзыв был успешно отправлен!"), language="en")
        else:
            await message.answer(f"<b>{message.from_user.full_name}</b> к сожалению вы уже отправляли свой отзыв", parse_mode="HTML")
    else:
        await message.answer(emoji.emojize(":cross_mark: Ошибка, попробуйте ещё раз"), language="en")


@admin_router.message(FormAdmin.sel_option)
async def sel_option_admin(message: Message, state=FSMContext):
    all_cities: dict = api.Weather().get_all_cities()
    city_text: str = message.text
    match message.text:
        case "Удалить отзыв":
            await message.answer(emoji.emojize(":bell: Вы выбрали пункт меню - <b>удалить</b>"), language="en", parse_mode="HTML")
        case "Узнать количество отзывов":
            await message.answer(emoji.emojize(":bell: Вы выбрали пункт меню - <b>количество отзывов</b>"), language="en", parse_mode="HTML")
        case "Уникальный отзыв":
            await message.answer(emoji.emojize(":bell: Вы выбрали пункт меню - <b>уникальный отзыв</b>"), language="en", parse_mode="HTML")


@admin_router.message()
async def process_callback_button(message: Message):
    all_cities: dict = api.Weather().get_all_cities()
    city_text: str = message.text
    if city_text in all_cities:
        city: str = all_cities.get(message.text)[-1]
        response_to_user: str = emoji.emojize(f":bell: Вы выбрали город: <b>{message.text}</b>", language="en", parse_mode="HTML")
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
        return emoji.emojize(":cross_mark: К сожалению ваш запрос не удался", language="HTML")