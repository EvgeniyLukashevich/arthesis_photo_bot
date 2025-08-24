from typing import Union, Type, Optional, Any

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
