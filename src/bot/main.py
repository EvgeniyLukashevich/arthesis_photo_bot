import asyncio
import logging
from src.bot import create_dispatcher, start_scheduler
from src.core import Config
from aiogram import Bot


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    )

    bot = Bot(token=Config.BOT_TOKEN)
    dp = create_dispatcher()

    try:
        # ЗАПУСКАЕМ ПЛАНИРОВЩИК
        start_scheduler(bot)
        # ЗАПУСКАЕМ БОТА
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(main())
