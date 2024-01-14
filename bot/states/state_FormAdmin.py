from aiogram.fsm.state import State, StatesGroup


class FormAdmin(StatesGroup):
    password = State()
    sel_option = State()
    sel_point = State()
