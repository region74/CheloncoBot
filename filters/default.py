from typing import Union

from aiogram import Router
from aiogram.filters import Filter
from aiogram.types import Message, CallbackQuery

router = Router()


class ChatUserFilter(Filter):
    def __init__(self, user_approve: list[int]) -> None:
        self.user_approve = user_approve

    async def __call__(self, update: Union[Message, CallbackQuery]) -> bool:
        if isinstance(update, Message):
            return update.from_user.id in self.user_approve
        elif isinstance(update, CallbackQuery):
            return update.from_user.id in self.user_approve
        else:
            return update.from_user.id in self.user_approve
