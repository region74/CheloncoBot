from aiogram import Router, F, Bot
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from database.orm_query import orm_send_device
from fsm.states import SendDevice

router = Router()


@router.callback_query(StateFilter(None), F.data == "send_device")
async def send_device(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('Укажите комментарий по отправке в ремонт:')
    await state.set_state(SendDevice.get_comment)


@router.message(SendDevice.get_comment)
async def send_device_comment(message: Message, state: FSMContext, bot: Bot, session: AsyncSession):
    if message.text:
        data = await state.get_data()
        add = {'comment': message.text}
        data.update(add)
        await orm_send_device(session, data)
        await state.clear()
        await message.answer('Спасибо! Данные сохранены ✅')
        await state.set_state(None)
    else:
        await message.answer('Укажите комментарий по отправке❗️')
