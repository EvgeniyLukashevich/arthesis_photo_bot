from aiogram.enums import ChatType

from src.core import Config
from aiogram import Dispatcher
from aiogram import types, F, Bot
from aiogram.dispatcher.router import Router

router = Router()


def incoming_message(user_name) -> str:
    return (f'Доброго времени суток, {user_name}!</b> \n\n'
            f'Я не предназначен для общения, но могу посоветовать вам подписаться на наш канал:'
            f'⬇️    ⬇️    ⬇️\n\n'
            f'<a href="{Config.CHANNEL_LINK}">ARThesis: библиотека фотоискусства</a> \n\n'
            f'Мы будем очень рады видеть Вас! ❤️\n'
            f'В нашем канале есть много интересного.'
)


@router.message(F.chat.type == ChatType.PRIVATE)
async def start_command(message: types.Message, bot: Bot):
    await bot.send_message(
        message.chat.id,
        parse_mode=Config.PARSE_MODE,
        text=incoming_message(
            user_name=f'{message.from_user.full_name}'
        )
    )


def register_incoming_messages_handlers(dp: Dispatcher):
    """Регистрация обработчиков модерации."""
    dp.include_router(router)