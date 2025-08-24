from aiogram import Dispatcher
from src.bot.handlers import register_handlers
from src.bot.scheduler import start_scheduler

__all__ = ["create_dispatcher", 'start_scheduler']


def create_dispatcher() -> Dispatcher:
    """
    Создает и настраивает экземпляр диспетчера Aiogram
    со всеми зарегистрированными обработчиками.
    Returns: экземпляр Dispatcher
    """
    dp = Dispatcher()
    register_handlers(dp)
    return dp
