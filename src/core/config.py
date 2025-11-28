from pathlib import Path
from dotenv import load_dotenv
import os
from aiogram.enums import ParseMode
from zoneinfo import ZoneInfo
from random import choice as random_choice

BASE_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(BASE_DIR / '.env')


class Config:
    BASE_DIR = Path(__file__).resolve().parent.parent.parent
    ADMIN_CHAT_ID = int(os.getenv('ADMIN_CHAT_ID'))
    DB_URL = os.getenv('DB_URL')
    PARSE_MODE = ParseMode.HTML
    CHANNEL_LINK = os.getenv('CHANNEL_LINK')
    TIMEZONE = ZoneInfo('Europe/Moscow')
    REGULAR_POST_HOUR_UTC = os.getenv('REGULAR_POST_HOUR_UTC', '5,10,11,15,16,17,18,19')
    INSTANT_CHECK_MINUTES = os.getenv('INSTANT_CHECK_MINUTES', '5,35')
    PRODUCTION_MODE = os.getenv('PRODUCTION_MODE', 'False').lower() == 'true'
    if PRODUCTION_MODE:
        CHAT_ID = int(os.getenv('CHAT_ID'))
        BOT_TOKEN = os.getenv('BOT_TOKEN')
        PHOTO_DIR = os.getenv('PROD_PHOTO_DIR')
    else:
        CHAT_ID = int(os.getenv('TEST_CHAT_ID'))
        BOT_TOKEN = os.getenv('TEST_BOT_TOKEN')
        PHOTO_DIR = os.getenv('TEST_PHOTO_DIR')

    @staticmethod
    def private_message(user_name) -> str:
        greetings = ['Доброго времени суток,', 'Рад приветствовать Вас,', 'Здравствуйте,', 'Салют,', 'Привет,']
        greeting = random_choice(greetings)
        return (f'{greeting} <b>{user_name}</b>!\n\n'
                f'Если Вы любите визуальное искусство, загляните в наши каналы — демонстрационные примеры работ '
                f'признанных авторов и, как следствие, ежедневное вдохновение и формирование правильной '
                f'насмотренности:\n\n'
                f'⬇️    ⬇️    ⬇️\n\n'
                f'<a href="{Config.CHANNEL_LINK}">ARThesis: фотоискусство</a> \n\n'
                f'<a href="">ARThesis: живопись</a> \n\n'
                f'Будем рады видеть Вас! ❤️\n')
