import bot.text
import emoji

from aiogram import types
from aiogram.filters.command import Command
from aiogram.types import FSInputFile
from bot.keyboards import kb, func_about_city_kb, func_neighbors_cities
from aiogram import Router
from aiogram.fsm.context import FSMContext

from database.services import admin_service
from bot.keyboards import review_text_butt
from bot.states import FormAdmin

router = Router()


@router.message(Command("help"))
async def help_command(message: types.Message):
    photo: FSInputFile = FSInputFile("bot/img/main_icon.jpg")
    await message.answer_photo(photo=photo, caption=emoji.emojize(bot.text[0] + emoji.emojize(bot.text[1]), language="en"), parse_mode="HTML")


@router.message(Command("start"))
async def start_command(message: types.Message):
    await message.answer(emoji.emojize(":bell: Выберите ваш <b>город</b>", language="en"), reply_markup=kb.start_kb, parse_mode="HTML")


@router.message(Command("name_city"))
async def about_city_command(message: types.Message):
    message_text: str = emoji.emojize(":bell: Выберите <b>город</b>", language="en")
    keyboard = func_about_city_kb()
    await message.answer(message_text, reply_markup=keyboard.as_markup(), parse_mode="HTML")


@router.message(Command("neighbors"))
async def neighbors_cities(message: types.Message):
    message_text: str = emoji.emojize(":bell: Выберите интересующий ваc <b>город</b>", language="en")
    keyboard_neighbors_cities = func_neighbors_cities()
    await message.answer(message_text, reply_markup=keyboard_neighbors_cities.as_markup(), parse_mode="HTML")


@router.message(Command("review"))
async def review_command(message: types.Message):
    await message.reply("Спасибо, что решили оставить нам свой отзыв!\nНапишите пожалуйста ваш отзыв.", reply_markup=review_text_butt().as_markup())


@router.message(Command("weather_5d"))
async def weather_5d(message: types.Message):
    await message.answer(emoji.emojize(":bell: Выберите город для прогноза на следующие <b>5 дней.</b>", language="en"), parse_mode="HTML", reply_markup=kb.kb_for_5d)

@router.message(Command("admin"))
async def admin_command(message: types.Message, state=FSMContext):
    response_to_admin_table = (await admin_service.get_one_admin(int(message.from_user.id)))[0][-1]
    if response_to_admin_table.tg_id == (message.from_user.id):
        await message.answer("Запуск авторизация для админа...")
        await state.set_state(FormAdmin.password)
        await message.answer("Введите пожалуйста ваш пароль: ")
    else:
        await message.answer("Для вас вход в админ панель запрещён")