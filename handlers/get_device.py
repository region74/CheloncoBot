import asyncio
import logging

from io import BytesIO
from aiogram import Router, F, Bot
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

# from keyboards.boards import main_kb, zp_month_kb, add_coments_kb
from fsm.states import GetDevice

# from scripts import import_vp as import_vp_script

router = Router()


@router.callback_query(StateFilter(None), F.data == "get_device")
async def import_zp(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('Укажите комментарий по приему:')
    await state.set_state(GetDevice.get_comment)


@router.message(GetDevice.get_comment)
async def get_device_comment(message: Message, state: FSMContext, bot: Bot):
    if message.text:
        await message.answer('Спасибо! Данные сохранены.')
        await state.set_state(None)
    else:
        await message.answer('Укажите комментарий по приемке!')
