from aiogram.enums import ChatType

from src.core import Config
from aiogram.filters import Command
from aiogram import Dispatcher
from aiogram import types, F, Bot
from aiogram.dispatcher.router import Router

router = Router()


def start_message(user_name) -> str:
    return (f'<b>Рад приветствовать Вас, {user_name}!</b> \n\n'
            f'Я не предназначен для общения, но могу предложить Вам подписаться на наши каналы:\n\n'
            f'⬇️    ⬇️    ⬇️\n\n'
            f'<a href="{Config.CHANNEL_LINK}">ARThesis: фотоискусство</a> \n\n'
            f'Мы будем очень рады видеть Вас! ❤️\n'
)


@router.message(
    Command("start"),
    F.chat.type == ChatType.PRIVATE
)
async def start_command(message: types.Message, bot: Bot):
    await bot.send_message(
        message.chat.id,
        parse_mode=Config.PARSE_MODE,
        text=start_message(
            user_name=f'{message.from_user.full_name}'
        )
    )


def register_start_handlers(dp: Dispatcher):
    """Регистрация обработчиков модерации."""
    dp.include_router(router)
