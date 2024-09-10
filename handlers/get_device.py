from aiogram import Router, F, Bot
from aiogram.filters import StateFilter
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from database.orm_query import orm_add_device
from fsm.states import GetDevice

router = Router()


@router.callback_query(StateFilter(None), F.data == "get_device")
async def get_device(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('Укажите комментарий по приему:')
    await state.set_state(GetDevice.get_comment)


@router.message(GetDevice.get_comment)
async def get_device_comment(message: Message, state: FSMContext, session: AsyncSession):
    if message.text:
        # TODO пример убрать
        data = {
            'number': float(124343421),
            'category': 'printer',
            'firma': 'hp',
            'model': 'm404dw'
        }
        await orm_add_device(session, data)

        await message.answer('Спасибо! Данные сохранены ✅')
        await state.set_state(None)
    else:
        await message.answer('Укажите комментарий по приемке❗️')
