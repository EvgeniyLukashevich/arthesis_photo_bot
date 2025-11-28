from aiogram.enums import ChatType

from src.core import Config
from aiogram import Dispatcher
from aiogram import types, F, Bot
from aiogram.dispatcher.router import Router

router = Router()


@router.message(F.chat.type == ChatType.PRIVATE)
async def start_command(message: types.Message, bot: Bot):
    await bot.send_message(
        message.chat.id,
        parse_mode=Config.PARSE_MODE,
        text=Config.private_message(user_name=message.from_user.full_name)
    )


def register_incoming_messages_handlers(dp: Dispatcher):
    """Регистрация обработчиков модерации."""
    dp.include_router(router)
