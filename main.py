import asyncio
import logging
import datetime

from aiogram import Bot, Dispatcher

from config import TOKEN_BOT
from handlers import default, get_device, send_device

# Устанавливаем часовой пояс Челябинска для логирования
logging.Formatter.converter = lambda *args: datetime.datetime.now(
    datetime.timezone(datetime.timedelta(hours=5))).timetuple()

logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%d/%m/%Y %H:%M:%S', level=logging.INFO)


async def main():
    logging.info('Запуск бота @chelonco174_bot')
    try:
        bot = Bot(token=TOKEN_BOT)
        dp = Dispatcher()
        dp.include_router(default.router)
        dp.include_router(get_device.router)
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    except Exception as e:
        logging.error(f'Произошла ошибка в работе бота:\n{e}')
        await main()


if __name__ == "__main__":
    asyncio.run(main())
