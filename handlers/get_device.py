from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from data.place import departments
from database.orm_query import orm_get_device, orm_update_device
from fsm.states import GetDevice
from keyboards.boards import device_place_change

router = Router()


@router.callback_query(StateFilter(None), F.data == "get_device")
async def get_device(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('Будем менять местоположение (отделение) устройства?',
                                  reply_markup=device_place_change())
    await state.set_state(GetDevice.get_place)


@router.callback_query(GetDevice.get_place)
async def query_place(callback: CallbackQuery, state: FSMContext):
    if callback.data == 'change_place':
        formatted_message = '\n'.join(f"{num}. {name}" for num, name in departments.items())
        await callback.message.answer(f'Укажите новый НОМЕР отделения из списка:\n {formatted_message}')
        await state.set_state(GetDevice.input_place)
    elif callback.data == 'skip_place':
        await callback.message.answer('Хорошо, тогда укажите комментарий:')
        await state.set_state(GetDevice.get_comment)
    else:
        await callback.message.answer('Неизвестная команда, сброс состояния...')
        await state.set_state(None)
        await state.clear()


@router.message(GetDevice.input_place)
async def input_place(message: Message, state: FSMContext, session: AsyncSession):
    if message.text.isdigit():
        target_place = int(message.text.lower())
        data = await state.get_data()
        add = {'place': target_place}
        data.update(add)
        await orm_update_device(session, data)
        await message.answer('Данные обновлены, теперь укажите комментарий:')
        await state.set_state(GetDevice.get_comment)
    else:
        await message.answer('Введите порядковый номер отделения, целым числом!')


@router.message(GetDevice.get_comment)
async def get_device_comment(message: Message, state: FSMContext, session: AsyncSession):
    if message.text:
        data = await state.get_data()
        add = {'comment': message.text}
        data.update(add)
        result = await orm_get_device(session, data)
        if result:
            await message.answer(result)
        else:
            await state.clear()
            await message.answer('Спасибо! Данные сохранены ✅')
            await state.set_state(None)
    else:
        await message.answer('Укажите комментарий по приемке❗️')
