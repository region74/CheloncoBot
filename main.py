import asyncio
import logging
import datetime

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config import TOKEN_BOT
from database.engine import create_db, drop_db, session_maker
from handlers import default, get_device, send_device
from middlewares.db import DataBaseSession

# Устанавливаем часовой пояс Челябинска для логирования
logging.Formatter.converter = lambda *args: datetime.datetime.now(
    datetime.timezone(datetime.timedelta(hours=5))).timetuple()

logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%d/%m/%Y %H:%M:%S', level=logging.INFO)

bot = Bot(token=TOKEN_BOT, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

async def on_startup(bot):
    run_param = False
    if run_param:
        await drop_db()
    await create_db()


async def on_shutdown(bot):
    logging.warning('Бот лег!')


async def main():
    logging.info('Запуск бота @chelonco174_bot')
    try:
        await create_db()

        dp.startup.register(on_startup)
        dp.shutdown.register(on_shutdown)
        dp.update.middleware(DataBaseSession(session_pool=session_maker))

        dp.include_router(default.router)
        dp.include_router(get_device.router)
        dp.include_router(send_device.router)

        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    except Exception as e:
        logging.error(f'Произошла ошибка в работе бота:\n{e}')
        await main()


if __name__ == "__main__":
    asyncio.run(main())
