import asyncio
import typer
from typing import Optional
from pathlib import Path
from src.database import AsyncSessionLocal
from src.models import InstantPost
from .utils import convert_msk_to_utc, post_activity_toggle, update_post_field, update_post_dates, add_post_dates

app = typer.Typer()


# ---------- Instant Post ----------
@app.command("add")
def add_instant(
        file: Path = typer.Option(..., "--file"),
        text: str = typer.Option(None, "--text"),
        tags: str = typer.Option(None, "--tags"),
        schedule: str = typer.Option(...,
                                     help='Даты через пробел в формате ДД.ММ.ГГГГ-ЧЧ:ММ (Московское время)'),
        active: bool = typer.Option(True, "--active/--no-active"),
):
    async def _add():
        async with AsyncSessionLocal() as db:
            db.add(InstantPost(
                photo_path=str(file.resolve()),
                text=text,
                tags=tags,
                schedule=convert_msk_to_utc(schedule),
                is_active=active,
            ))
            await db.commit()

    asyncio.run(_add())
    typer.echo("    ✅  Внеочередной пост добавлен")


@app.command("deactivate")
def deactivate_instant(post_id: int):
    """Внеочередной пост. Изменить статус на неактивный."""
    try:
        result = asyncio.run(post_activity_toggle(
            model=InstantPost,
            post_id=post_id,
            active_status=False)
        )
        if result:
            typer.secho(f"    ✅  Внеочередной Пост id={post_id} деактивирован", fg=typer.colors.GREEN)

    except Exception as e:
        typer.secho(
            f"    ❌  При попытке смены статуса is_active "
            f"Внеочередного Поста id={post_id} произошла непредвиденная ошибка\n"
            f"{e}",
            fg=typer.colors.RED
        )


@app.command("activate")
def activate_instant(post_id: int):
    """Внеочередной пост. Изменить статус на активный."""

    try:
        result = asyncio.run(post_activity_toggle(
            model=InstantPost,
            post_id=post_id,
            active_status=True)
        )
        if result:
            typer.secho(f"    ✅  Внеочередной Пост id={post_id} активирован", fg=typer.colors.GREEN)

    except Exception as e:
        typer.secho(
            f"    ❌  При попытке смены статуса is_active "
            f"Внеочередного Поста id={post_id} произошла непредвиденная ошибка\n"
            f"{e}",
            fg=typer.colors.RED
        )


@app.command('set-photo-path')
def set_photo_path(
        post_id: int = typer.Argument(..., help='ID внеочередного поста'),
        photo_path: Optional[str] = typer.Option(
            None, '--value', help='Новый фото-файл внеочередного поста. '
        ),
):
    """Внеочередной пост. Изменить путь до фото-файла."""

    asyncio.run(update_post_field(
        model=InstantPost,
        post_id=post_id,
        field_name='photo_path',
        value=photo_path,
        success_message=f"    ✅  ВНЕОЧЕРЕДНОЙ ПОСТ {post_id} :: Путь до фото-файла обновлен."
    ))


@app.command('set-text')
def set_text(
        post_id: int = typer.Argument(..., help='ID внеочередного поста'),
        text: Optional[str] = typer.Option(
            None, '--value', help='Новый текст внеочередного поста. '
        ),
):
    """Внеочередной пост. Изменить текст поста."""

    asyncio.run(update_post_field(
        model=InstantPost,
        post_id=post_id,
        field_name='text',
        value=text,
        success_message=f"    ✅  ВНЕОЧЕРЕДНОЙ ПОСТ {post_id} :: Текст поста обновлен."
    ))


@app.command('set-tags')
def set_tags(
        post_id: int = typer.Argument(..., help='ID внеочередного поста'),
        tags: Optional[str] = typer.Option(
            None, '--value', help='Новые тэги внеочередного поста. '
                                  'Перечисление тэгов через пробел.'
        ),
):
    """Внеочередной пост. Изменить тэги поста."""

    asyncio.run(update_post_field(
        model=InstantPost,
        post_id=post_id,
        field_name='tags',
        value=tags,
        success_message=f"    ✅  ВНЕОЧЕРЕДНОЙ ПОСТ {post_id} :: Тэги поста обновлены."
    ))


@app.command('set-dates')
def set_dates(
        post_id: int = typer.Argument(..., help='ID внеочередного поста'),
        dates: Optional[str] = typer.Option(
            None, '--value', help='Новое расписание внеочередного поста. '
                                  'Перечисление дат через пробел (по МСК). '
                                  'ДД.ММ.ГГГГ-ЧЧ:ММ'
        ),
):
    """Внеочередной пост. Изменить расписание публикации поста."""

    asyncio.run(update_post_dates(
        model=InstantPost,
        post_id=post_id,
        value=dates,
        success_message=f"    ✅  ВНЕОЧЕРЕДНОЙ ПОСТ {post_id} :: Расписание поста обновлено."
    ))


@app.command('add-dates')
def add_dates(
        post_id: int = typer.Argument(..., help='ID внеочередного поста'),
        dates: Optional[str] = typer.Option(
            None, '--value', help='Добавление дат в расписание внеочередного поста. '
                                  'Перечисление дат через пробел (по МСК). '
                                  'ДД.ММ.ГГГГ-ЧЧ:ММ'
        ),
):
    """Внеочередной пост. Добавить даты в расписание публикации поста."""

    asyncio.run(add_post_dates(
        model=InstantPost,
        post_id=post_id,
        value=dates,
        success_message=f"    ✅  ВНЕОЧЕРЕДНОЙ ПОСТ {post_id} :: В расписание поста добавлены новые даты."
    ))
