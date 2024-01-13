import api
import emoji

from aiogram import F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram import Router

from bot import review_text_butt
from bot import FormReview
from database.services import review_service
from bot.text import about_of_city, neighbors_city


fsm_router = Router()


@fsm_router.callback_query(F.data.endswith("_nbt"))
async def callback_review_response(callback_review: CallbackQuery, state=FSMContext):
    if callback_review.data == "Yes_nbt":
        await state.set_state(FormReview.name)
        await callback_review.message.answer("Введите пожалуйста ваше имя")
    else:
        await callback_review.answer("Форма отправки отзыва отменена.")
        await state.clear()


@fsm_router.callback_query()
async def callback_response_info_city(callback: CallbackQuery):
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
