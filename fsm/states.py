from aiogram.fsm.state import StatesGroup, State


class GetDevice(StatesGroup):
    get_comment = State()
