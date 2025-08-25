from typing import Union, Type, Optional, Any
from pathlib import Path
import typer
from sqlalchemy import update
from src.database import AsyncSessionLocal
from src.models import Post, AdPost, InstantPost
from datetime import datetime, timezone
from src.core import Config


def convert_msk_to_utc(dates_str: str) -> list[str]:
    """Конвертирует строку с датами из MSK в UTC.

    Формат входных данных: "ДД.ММ.ГГГГ-ЧЧ:ММ ДД.ММ.ГГГГ-ЧЧ:ММ ..."
    Возвращает список строк в ISO-формате UTC.
    """
    return [
        datetime.strptime(d, "%d.%m.%Y-%H:%M")
        .replace(tzinfo=Config.TIMEZONE)
        .astimezone(timezone.utc)
        .isoformat()
        for d in dates_str.split()
    ]


async def post_activity_toggle(
        model: Type[Union[Post, AdPost, InstantPost]],
        post_id: int,
        active_status: bool
):
    async with AsyncSessionLocal() as db:
        result = await db.execute(
            update(model).where(model.id == post_id).values(is_active=active_status)
        )
        if result.rowcount == 0:
            typer.secho(f"    ❌  Регулярный Пост id={post_id} не найден.", fg=typer.colors.RED)
            return False
        await db.commit()
        return True


async def update_post_field(
        model: Type[Union[Post, AdPost, InstantPost]],
        post_id: int,
        field_name: str,
        value: Optional[Any],
        success_message: str,
        error_message: str = "    ❌  Пост с ID {post_id} не найден!"
) -> bool:
    """Обновляет любое поле любого типа поста"""
    async with AsyncSessionLocal() as db:
        post = await db.get(model, post_id)
        if not post:
            typer.secho(error_message.format(post_id=post_id), fg=typer.colors.RED)
            return False
        setattr(post, field_name, value)
        await db.commit()
        typer.secho(success_message, fg=typer.colors.GREEN)
        return True


async def update_post_dates(
        model: Type[Union[AdPost, InstantPost]],
        post_id: int,
        value: Optional[Any],
        success_message: str,
        error_message: str = "    ❌  Пост с ID {post_id} не найден!"
) -> bool:
    """Полностью обновить список дат публикации"""
    async with AsyncSessionLocal() as db:
        post = await db.get(model, post_id)
        if not post:
            typer.secho(error_message.format(post_id=post_id), fg=typer.colors.RED)
            return False
        post.schedule = convert_msk_to_utc(value)
        await db.commit()
        typer.secho(success_message, fg=typer.colors.GREEN)
        return True


async def add_post_dates(
        model: Type[Union[AdPost, InstantPost]],
        post_id: int,
        value: Optional[Any],
        success_message: str,
        error_message: str = "    ❌  Пост с ID {post_id} не найден!"
) -> bool:
    """Добавить список дат публикации к уже существующим"""
    async with AsyncSessionLocal() as db:
        post = await db.get(model, post_id)
        if not post:
            typer.secho(error_message.format(post_id=post_id), fg=typer.colors.RED)
            return False
        value_utc = convert_msk_to_utc(value)
        post.schedule = list(set(post.schedule + value_utc))
        await db.commit()
        typer.secho(success_message, fg=typer.colors.GREEN)
        return True


def parse_filename(filename: str) -> dict:
    """
    Парсит имя файла в формате:
    Photo-Title+Photo-Location+Photo-Date+Photo-Tag1+Photo-Tag2+....jpg
    """
    # Убираем расширение файла
    name_without_ext = Path(filename).stem

    # Разбиваем по '+'
    parts = name_without_ext.split('+')

    result = {
        'title': None,
        'location': None,
        'date': None,
        'tags': None
    }

    for part in parts:
        # Основная информация о фото
        if 'Title' in part:
            title_value = part.replace('Title', '').strip('=').replace('$', ' ')
            result['title'] = title_value if title_value else None
        elif 'Location' in part:
            location_value = part.replace('Location', '').strip('=').replace('$', ' ')
            result['location'] = location_value if location_value else None
        elif 'Date' in part:
            date_value = part.replace('Date', '').strip('=').replace('$', ' ')
            result['date'] = date_value if date_value else None

        else:
            # Теги
            tags_value = part.replace('Tags', '').strip('=').replace('$', ' ')
            result['tags'] = tags_value if tags_value else None

    return result

if __name__ == '__main__':
    filename = 'Title=Красота$Природы+Location=Нью-Йорк+Date=22$Июня$1965+Tags=пейзаж$портрет$мария_чудвел.jpg'

    print(parse_filename(filename))