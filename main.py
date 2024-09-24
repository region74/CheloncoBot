import asyncio
import logging
import datetime

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config import TOKEN_BOT
from database.engine import create_db, session_maker
from handlers import default, get_device, send_device
from middlewares.db import DataBaseSession

# Устанавливаем часовой пояс Челябинска для логирования
logging.Formatter.converter = lambda *args: datetime.datetime.now(
    datetime.timezone(datetime.timedelta(hours=5))).timetuple()

logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%d/%m/%Y %H:%M:%S', level=logging.INFO)

bot = Bot(token=TOKEN_BOT, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()


async def on_startup():
    await create_db()


async def main():
    logging.info('Запуск бота @chelonco174_bot')
    try:
        dp.startup.register(on_startup)
        dp.update.middleware(DataBaseSession(session_pool=session_maker))
        dp.include_routers(default.router, get_device.router, send_device.router)

        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    except Exception as e:
        logging.error(f'Произошла ошибка в работе бота:\n{e}')
        await main()


if __name__ == "__main__":
    asyncio.run(main())
