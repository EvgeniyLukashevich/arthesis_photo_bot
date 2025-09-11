from pathlib import Path
from dotenv import load_dotenv
import os
from aiogram.enums import ParseMode
from zoneinfo import ZoneInfo

BASE_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(BASE_DIR / '.env')


class Config:
    BASE_DIR = Path(__file__).resolve().parent.parent.parent
    BOT_TOKEN = os.getenv('BOT_TOKEN')
    ADMIN_CHAT_ID = int(os.getenv('ADMIN_CHAT_ID'))
    CHAT_ID = int(os.getenv('CHAT_ID'))
    DB_URL = os.getenv('DB_URL')
    PHOTOS_DIR = Path(os.getenv('PHOTOS_DIR', BASE_DIR / 'photos'))
    PARSE_MODE = ParseMode.HTML
    CHANNEL_LINK = os.getenv('CHANNEL_LINK')
    TIMEZONE = ZoneInfo('Europe/Moscow')
    REGULAR_POST_HOUR_UTC = os.getenv('REGULAR_POST_HOUR_UTC', '5,10,11,15,16,17,18,19')
    INSTANT_CHECK_MINUTES = os.getenv('INSTANT_CHECK_MINUTES', '5,35')
    PRODUCTION_MODE = os.getenv('PRODUCTION_MODE', 'False').lower() == 'true'
    if PRODUCTION_MODE:
        PHOTO_DIR = os.getenv('PROD_PHOTO_DIR')
    else:
        PHOTO_DIR = os.getenv('TEST_PHOTO_DIR')

