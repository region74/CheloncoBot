from aiogram import Router, F
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters.command import CommandObject, Command

from keyboards.boards import device_kb

router = Router()


@router.message(StateFilter(None), CommandStart())
async def command_help(message: Message, command: CommandObject) -> None:
    device_data = command.args
    if device_data:
        info = device_data.split('_')
        type = info[0]
        company = info[1]
        model = info[2]
        invenarny = info[3]
        place = info[4]
        await message.answer(
            f'Распознано устройство✅\nТип: {type}\nФирма: {company}\nМодель: {model}\nИнв.номер: {invenarny}\nМесто: {place}')
        await message.answer('Что с ним делать?', reply_markup=device_kb())
    else:
        await message.answer('Устройство не распознано! ⚠️\nПроверьте корректность QR-кода')


@router.message(StateFilter(None), Command('help'))
async def command_help(message: Message) -> None:
    await message.answer(f'При возникновении проблем или багов: {"https://t.me/ignatov23"}')


@router.message(StateFilter(None), Command('info'))
async def command_help(message: Message) -> None:
    await message.answer(f'Полноценная инструкция по работе с ботом появится после реализации функционала')


@router.message(StateFilter(None))
async def any_message(message: Message) -> None:
    await message.answer('Бот в разработке и тестировании')
