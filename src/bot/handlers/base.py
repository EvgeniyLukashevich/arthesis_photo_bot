from aiogram import Dispatcher
from .start import register_start_handlers
from .incoming_message import register_incoming_messages_handlers


def register_handlers(dp: Dispatcher):
    """Главный регистратор всех обработчиков"""
    register_start_handlers(dp)
    register_incoming_messages_handlers(dp)
