from aiogram import Router, F
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters.command import CommandObject, Command
from sqlalchemy.ext.asyncio import AsyncSession

from config import APPROVE_USERS
from database.orm_query import orm_add_device
from filters.default import ChatUserFilter
from keyboards.boards import device_kb

router = Router()

# Фильтрация разрешенных пользователей
router.message.filter(ChatUserFilter(APPROVE_USERS))
router.callback_query.filter(ChatUserFilter(APPROVE_USERS))


@router.message(StateFilter(None), CommandStart())
async def command_start(message: Message, state: FSMContext, command: CommandObject, session: AsyncSession) -> None:
    device_data = command.args
    if device_data:
        info = device_data.split('_')
        invenarny = info[3].replace('-', '/')
        type = info[0]
        company = info[1]
        model = info[2]
        await message.answer(
            f'Распознано устройство✅')
        data = {
            'number': str(invenarny),
            'category': str(type),
            'model': str(model),
            'firma': str(company)
        }
        result = await orm_add_device(session, data)
        if result:
            await message.answer(result)
        await state.update_data(**data)
        await message.answer('Что с ним делать?', reply_markup=device_kb())
    else:
        await message.answer('Устройство не распознано! ⚠️\nПроверьте корректность QR-кода')


@router.callback_query(StateFilter(None), F.data == "no_trigger")
async def cancle_process(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('Хорошо, процесс завершен.')
    await state.clear()
    await state.set_state(None)


@router.message(StateFilter(None), Command('help'))
async def command_help(message: Message) -> None:
    await message.answer(f'При возникновении проблем или багов: {"https://t.me/ignatov23"}')


@router.message(StateFilter(None), Command('report'))
async def command_report(message: Message) -> None:
    await message.answer(f'Какой отчет нужно получить?')


@router.message(StateFilter(None), Command('info'))
async def command_info(message: Message) -> None:
    await message.answer(f'Полноценная инструкция по работе с ботом появится после реализации функционала')


@router.message(StateFilter(None))
async def any_message(message: Message) -> None:
    await message.answer('Бот в разработке и тестировании')
