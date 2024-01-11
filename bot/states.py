from aiogram.fsm.state import StatesGroup, State


class FormReview(StatesGroup):
    name = State()
    age = State()
    review_text = State()