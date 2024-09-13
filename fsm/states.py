from aiogram.fsm.state import StatesGroup, State


class GetDevice(StatesGroup):
    get_place = State()
    input_place = State()
    get_comment = State()


class SendDevice(StatesGroup):
    get_place = State()
    input_place = State()
    get_comment = State()
