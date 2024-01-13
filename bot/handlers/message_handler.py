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
        await message.answer("Успешно. Добро пожаловать в админ панель %s" % message.from_user.full_name)
        await state.set_state(FormAdmin.sel_option)
        await message.answer("Выберите пункт меню %s" % message.from_user.full_name, reply_markup=get_admin_bt())
    else:
        await message.answer("Пароль неверен")


@admin_router.message(FormReview.name)
async def name_user(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(FormReview.age)
    await message.answer("Введите свой возраст")


@admin_router.message(FormReview.age)
async def age_user(message: Message, state: FSMContext):
    if message.text.isdigit():
        await state.update_data(age=int(message.text))
        await state.set_state(FormReview.review_text)
        await message.answer("Замечательно, теперь напишите свой отзыв")
    else:
        await message.answer("Неверно был введён возраст")


@admin_router.message(FormReview.review_text)
async def review_text_from_user(message: Message, state: FSMContext):
    if await state.update_data(review_text=message.text):
        await message.answer("Успешно! Спасибо за ваш отзыв.")
        state_data = await state.get_data()
        await state.clear()
        data_for_user: list = [state_data.get(key) for key in state_data.keys()]
        data_for_user.insert(0, message.from_user.id)
        review_obj: tuple = data_for_user[0], data_for_user[-1], data_for_user[1], data_for_user[2]
        result = await review_service.get_one_reviews(data_for_user[0])
        if len(result) == 0:
            await review_service.add_one_reviews(*review_obj)
            await message.answer(f"{message.from_user.full_name} ваш отзыв был успешно отправлен!")
        else:
            await message.answer(f"{message.from_user.full_name} к сожалению вы уже отправляли свой отзыв")
    else:
        await message.answer("Ошибка, попробуйте ещё раз")


@admin_router.message(FormAdmin.sel_option)
async def sel_option_admin(message: Message, state=FSMContext):
    all_cities: dict = api.Weather().get_all_cities()
    city_text: str = message.text
    match message.text:
        case "Удалить отзыв":
            await message.answer("Вы выбрали пункт меню удалить")
        case "Узнать количество отзывов":
            await message.answer("Вы выбрали пункт меню - количество отзывов")
        case "Уникальный отзыв":
            await message.answer("Вы выбрали пункт меню - уникальный отзыв")            


@admin_router.message()
async def process_callback_button(message: Message):
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