import aiogram.exceptions
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram import Bot, exceptions, types
from aiogram.types import FSInputFile
from src.database import AsyncSessionLocal
from src.models import Post, AdPost, InstantPost
from sqlalchemy import select, func, update
from datetime import datetime, timezone
from src.core import Config
from random import choice as random_choice
from random import randint as random_int
import asyncio
import logging

sched = AsyncIOScheduler()

logger = logging.getLogger(__name__)

DEFAULT_CAPTION = (f'📸 <b>УВАЖАЕМЫЕ ПОДПИСЧИКИ!</b> 📸\n\n'
                   f'Мы невероятно рады видеть Вас на нашем канале!\n'
                   f'И хотим выразить Вам огромную благодарность за '
                   f'Вашу обратную связь!\n\n'
                   f'ОГРОМНОЕ СПАСИБО!  ♥️ ♥️ ♥️')

REGULAR_POST_REACTIONS = ['❤', '👍', '🔥', '👏', '😱', '🤩', '👌', '😍', '💯']


def instant_post_caption(instant_post: InstantPost):
    result = ''

    if instant_post.text:
        result += f'{instant_post.text}\n'

    if instant_post.tags:
        result += f'\n'
        tag_list = instant_post.tags.split()
        for tag in tag_list:
            result += f'#{tag}  '

    return result.replace('****', '\n')


def ad_post_caption(ad_post: AdPost):
    result = 'Реклама\n'

    if ad_post.erid:
        result += f'erid: {ad_post.erid}\n'

    if ad_post.advertiser_name:
        result += f'{ad_post.advertiser_name}\n'

    if ad_post.advertiser_link:
        result += f'{ad_post.advertiser_link}\n'

    if ad_post.title:
        result += f'\n{ad_post.title}\n'

    if ad_post.text:
        result += f'\n{ad_post.text}\n'

    if ad_post.link:
        result += f'\n{ad_post.link}\n'

    if ad_post.tags:
        result += f'\n'
        tag_list = ad_post.tags.split()
        for tag in tag_list:
            result += f'#{tag}  '

    return result.replace('****', '\n')


def regular_post_caption(regular_post: Post):
    result = ''

    if regular_post.header:
        result += f'<i>{regular_post.header}</i>\n\n'
    # else:
    #     result += f'📷\n\n'

    if regular_post.title:
        result += f'<b>{regular_post.title}</b>\n\n'

    if regular_post.author:
        result += f'Автор: <b>{regular_post.author}</b>\n'

    if regular_post.date and regular_post.location:
        result += f'{regular_post.location}; {regular_post.date}\n'
    else:
        if regular_post.date:
            result += f'{regular_post.date}\n'
        if regular_post.location:
            result += f'{regular_post.location}\n'

    if regular_post.caption:
        result += f'\n<blockquote><i>{regular_post.caption}</i></blockquote>\n'

    if regular_post.tags:
        result += f'\n'
        tag_list = regular_post.tags.split()
        for tag in tag_list:
            result += f'#{tag}  '

    return result.replace('****', '\n')


async def send_post(bot: Bot, post: Post):
    max_retries = 10
    retry_delay = 15

    for attempt in range(max_retries):
        try:
            logger.info(f"🖼️ Отправка поста {post.id} в чат {Config.CHAT_ID}")

            if isinstance(post, Post):
                caption = regular_post_caption(post)
            elif isinstance(post, AdPost):
                caption = ad_post_caption(post)
            elif isinstance(post, InstantPost):
                caption = instant_post_caption(post)
            else:
                caption = DEFAULT_CAPTION
                await bot.send_message(
                    chat_id=Config.CHAT_ID,
                    text=caption,
                    parse_mode=Config.PARSE_MODE
                )
                await bot.send_message(
                    chat_id=Config.ADMIN_CHAT_ID,
                    text='НЕПОЛАДКА С ОПРЕДЕЛЕНИЕМ КЛАССА '
                         'ОТПРАВЛЯЕМОГО ПОСТА\n'
                         'src/scheduler.py/send_post()'
                )
                return

            logger.debug(f"📨 Отправляю фото в Telegram API...")

            photo_path = post.photo_path.replace('@', Config.PHOTO_DIR)

            if Config.PRODUCTION_MODE:
                photo_path = photo_path.replace('\\', '/')
            else:
                photo_path = photo_path.replace('/', '\\')

            result = await bot.send_photo(
                chat_id=Config.CHAT_ID,
                photo=FSInputFile(photo_path),
                caption=caption,
                parse_mode=Config.PARSE_MODE
            )

            await add_reaction_to_post(bot, result.message_id)

            if attempt > 1:
                await bot.send_message(chat_id=Config.ADMIN_CHAT_ID, text=f'Сообщение {result.message_id} '
                                                                          f'наконец отправлено.')

            logger.info(f"✅ Пост отправлен успешно! Message ID: {result.message_id}")

            break

        except aiogram.exceptions.TelegramNetworkError as e:
            error_message_for_admin = (f'ARThesis: фотоискусство. Проблема со связью и отправкой поста.\n\n'
                                       f'Повторная отправка. Попытка # {attempt}\n\n'
                                       f'ERROR: \n{e}')
            await bot.send_message(chat_id=Config.ADMIN_CHAT_ID, text=error_message_for_admin)
            if attempt < max_retries - 1:
                await asyncio.sleep(retry_delay)
            else:
                raise e
        except exceptions.TelegramForbiddenError as e:
            logger.error(f"🚫 Бот заблокирован или не имеет доступа к чату: {e}")
        except exceptions.TelegramBadRequest as e:
            logger.error(f"❌ Неверный запрос к Telegram API: {e}")
        except Exception as e:
            logger.error(f"💥 Критическая ошибка отправки: {e}")
            import traceback
            logger.error(traceback.format_exc())


async def add_reaction_to_post(bot: Bot, message_id: int):
    try:
        time_delay = random_int(3, 15)
        reactions_list = REGULAR_POST_REACTIONS
        reaction = random_choice(reactions_list)
        await asyncio.sleep(time_delay)
        await bot.set_message_reaction(
            chat_id=Config.CHAT_ID,
            message_id=message_id,
            reaction=[types.ReactionTypeEmoji(emoji=reaction)],
            is_big=False
        )

        logger.info(f"🎭 Добавлена реакция '{reaction}' к сообщению {message_id}")

    except exceptions.TelegramBadRequest as e:
        if "message reaction not allowed" in str(e).lower():
            logger.warning("⚠️ Реакции не разрешены в этом чате/канале")
        else:
            logger.error(f"❌ Ошибка при добавлении реакции: {e}")

    except Exception as e:
        logger.error(f"💥 Ошибка в add_reaction_to_post: {e}")


async def publish_regular_post(bot: Bot):
    logger.info("⏰ Запуск publish_regular_post")

    try:
        async with AsyncSessionLocal() as db:
            stmt = (
                select(Post)
                .where(Post.is_active == True, Post.shown == False)
                .order_by(func.random())
                .limit(1)
            )
            post = (await db.execute(stmt)).scalar_one_or_none()

            logger.info(f"📊 Найден пост для публикации: {post}")

            if not post:
                logger.info("📭 Активные непоказанные посты не найдены, сбрасываю флаги shown")
                # все показаны — сброс
                await db.execute(
                    update(Post).where(Post.is_active == True).values(shown=False)
                )
                await db.commit()
                post = (await db.execute(stmt)).scalar_one_or_none()
                logger.info(f"🔄 После сброса найден пост: {post}")

            if post:
                post.shown = True
                await db.commit()
                logger.info(f"📤 Публикую пост: {post.title}")
                await send_post(bot, post)
                logger.info(f"✅ Пост опубликован: {post.title}")
            else:
                logger.warning("⚠️ Посты для публикации не найдены даже после сброса")

    except Exception as e:
        logger.error(f"❌ Ошибка в publish_regular_post: {e}")
        import traceback
        logger.error(traceback.format_exc())


async def publish_instant_or_ad(bot: Bot):
    now_utc = datetime.now(timezone.utc)
    now_msk = now_utc.astimezone(Config.TIMEZONE)  # Текущее время в MSK

    async def _publish_post(publishing_post, db_session, time_msk):
        remaining_times = []
        should_send = False

        for scheduled_time_utc in publishing_post.schedule:
            scheduled_time = datetime.fromisoformat(scheduled_time_utc).astimezone(Config.TIMEZONE)

            if scheduled_time <= time_msk:
                print(f'  НАЗНАЧЕННОЕ (МСК):  {scheduled_time}')
                print(f"       СЕЙЧАС (МСК):  {time_msk}")
                should_send = True  # Нужно отправить пост
            else:
                remaining_times.append(scheduled_time_utc)  # Оставляем для будущих публикаций

        if should_send:
            await send_post(bot, publishing_post)

            # Обновляем расписание
            if remaining_times:
                # Если остались будущие публикации - обновляем schedule
                publishing_post.schedule = remaining_times
            else:
                # Если это была последняя публикация - деактивируем
                publishing_post.is_active = False

            await db_session.commit()

    async with AsyncSessionLocal() as db:
        # InstantPost по расписанию
        instant_stmt = select(InstantPost).where(InstantPost.is_active == True)
        instant_posts = (await db.execute(instant_stmt)).scalars().all()

        for post in instant_posts:
            await _publish_post(post, db, now_msk)

        # AdPost по расписанию
        ad_stmt = select(AdPost).where(AdPost.is_active == True)
        ad_posts = (await db.execute(ad_stmt)).scalars().all()

        for post in ad_posts:
            await _publish_post(post, db, now_msk)


def start_scheduler(bot: Bot):
    sched.add_job(
        publish_regular_post,
        # trigger="cron",
        # hour=Config.REGULAR_POST_HOUR_UTC,
        # minute=0,
        # timezone='UTC',
        trigger='interval',
        minutes=1,
        args=[bot],
    )
    sched.add_job(
        publish_instant_or_ad,
        trigger="cron",
        minute=Config.INSTANT_CHECK_MINUTES,
        timezone='UTC',
        args=[bot],
    )
    sched.start()
