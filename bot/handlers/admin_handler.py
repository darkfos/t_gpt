from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from bot import FormAdmin
from database.services import admin_service


admin_router = Router()


@admin_router.message(Command("admin"))
async def admin_command(message: Message, state=FSMContext):
    response_to_admin_table = (await admin_service.get_one_admin(int(message.from_user.id)))[0][-1]
    if response_to_admin_table.tg_id == (message.from_user.id):
        await message.answer("Запуск авторизация для админа...")
        await state.set_state(FormAdmin.password)
        await message.answer("Введите пожалуйста ваш пароль: ")
    else:
        await message.answer("Для вас вход в админ панель запрещён")

@admin_router.message(FormAdmin.password)
async def password_admin(message: Message, state=FSMContext):
    password_admin: str = message.text
    response_to_admin_table = (await admin_service.get_one_admin(int(message.from_user.id)))[0][-1]
    if response_to_admin_table.password == password_admin:
        await message.answer("Успешно. Добро пожаловать в админ панель %s" % message.from_user.full_name)
    else:
        await message.answer("Пароль неверен")

