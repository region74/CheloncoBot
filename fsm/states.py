from aiogram.fsm.state import StatesGroup, State


class GetDevice(StatesGroup):
    get_comment = State()

class SendDevice(StatesGroup):
    get_comment = State()
