from aiogram import F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram import Router

from bot import review_text_butt
from bot import FormReview
from database.services import review_service
from database.models import Review


fsm_router = Router()


@fsm_router.message(Command("review"))
async def review_command(message: Message):
    await message.reply("Спасибо, что решили оставить нам свой отзыв!\nНапишите пожалуйста ваш отзыв.", reply_markup=review_text_butt().as_markup())


@fsm_router.callback_query(F.data.endswith("_nbt"))
async def callback_review_response(callback_review: CallbackQuery, state=FSMContext):
    if callback_review.data == "Yes_nbt":
        await state.set_state(FormReview.name)
        await callback_review.message.answer("Введите пожалуйста ваше имя")
    else:
        await callback_review.answer("Форма отправки отзыва отменена.")
        await state.clear()


@fsm_router.message(FormReview.name)
async def name_user(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(FormReview.age)
    await message.answer("Введите свой возраст")


@fsm_router.message(FormReview.age)
async def age_user(message: Message, state: FSMContext):
    if message.text.isdigit():
        await state.update_data(age=int(message.text))
        await state.set_state(FormReview.review_text)
        await message.answer("Замечательно, теперь напишите свой отзыв")
    else:
        await message.answer("Неверно был введён возраст")


@fsm_router.message(FormReview.review_text)
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
