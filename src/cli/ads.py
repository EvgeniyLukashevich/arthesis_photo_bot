import asyncio
import typer
from typing import Optional
from pathlib import Path
from src.database import AsyncSessionLocal
from src.models import AdPost
from .utils import post_activity_toggle, convert_msk_to_utc, update_post_field, update_post_dates, add_post_dates

app = typer.Typer()


# ---------- Ad Post ----------
@app.command("add")
def add_ad(
        file: Path = typer.Option(..., "--file"),
        erid: str = typer.Option(None, "--erid"),
        advertiser_name: str = typer.Option(None, "--advertiser_name"),
        advertiser_link: str = typer.Option(None, "--advertiser_link"),
        title: str = typer.Option(None, "--title"),
        text: str = typer.Option(None, "--text"),
        link: str = typer.Option(None, "--link"),
        schedule: str = typer.Option(...,
                                     help='Даты через пробел в формате ДД.ММ.ГГГГ-ЧЧ:ММ (Московское время)'),
        tags: str = typer.Option(None, "--tags"),
        active: bool = typer.Option(True, "--active/--no-active"),
):
    async def _add():
        async with AsyncSessionLocal() as db:
            db.add(AdPost(
                photo_path=str(file.resolve()),
                erid=erid,
                advertiser_name=advertiser_name,
                advertiser_link=advertiser_link,
                title=title,
                text=text,
                link=link,
                schedule=convert_msk_to_utc(schedule),
                tags=tags,
                is_active=active,
            ))
            await db.commit()

    asyncio.run(_add())
    typer.echo("    ✅  Рекламный Пост добавлен")


@app.command("deactivate")
def deactivate_ad(post_id: int):
    """Рекламный пост. Изменить статус на неактивный."""
    try:
        result = asyncio.run(post_activity_toggle(
            model=AdPost,
            post_id=post_id,
            active_status=False)
        )
        if result:
            typer.secho(f"    ✅  Рекламный Пост id={post_id} деактивирован", fg=typer.colors.GREEN)

    except Exception as e:
        typer.secho(
            f"    ❌  При попытке смены статуса is_active "
            f"Рекламного Поста id={post_id} произошла непредвиденная ошибка\n"
            f"{e}",
            fg=typer.colors.RED
        )


@app.command("activate")
def activate_ad(post_id: int):
    """Рекламный пост. Изменить статус на активный."""

    try:
        result = asyncio.run(post_activity_toggle(
            model=AdPost,
            post_id=post_id,
            active_status=True)
        )
        if result:
            typer.secho(f"    ✅  Рекламный Пост id={post_id} активирован", fg=typer.colors.GREEN)

    except Exception as e:
        typer.secho(
            f"    ❌  При попытке смены статуса is_active "
            f"Рекламного Поста id={post_id} произошла непредвиденная ошибка\n"
            f"{e}",
            fg=typer.colors.RED
        )


@app.command('set-photo-path')
def set_photo_path(
        post_id: int = typer.Argument(..., help='ID рекламного поста'),
        photo_path: Optional[str] = typer.Option(
            None, '--value', help='Новый фото-файл рекламного поста. '
        ),
):
    """Рекламный пост. Изменить путь до фото-файла."""

    asyncio.run(update_post_field(
        model=AdPost,
        post_id=post_id,
        field_name='photo_path',
        value=photo_path,
        success_message=f"    ✅  РЕКЛАМНЫЙ ПОСТ {post_id} :: Путь до фото-файла обновлен."
    ))


@app.command('set-erid')
def set_erid(
        post_id: int = typer.Argument(..., help='ID рекламного поста'),
        erid: Optional[str] = typer.Option(
            None, '--value', help='Новый erid рекламного поста. '
        ),
):
    """Рекламный пост. Изменить erid."""

    asyncio.run(update_post_field(
        model=AdPost,
        post_id=post_id,
        field_name='erid',
        value=erid,
        success_message=f"    ✅  РЕКЛАМНЫЙ ПОСТ {post_id} :: Erid обновлен."
    ))


@app.command('set-advertiser-name')
def set_advertiser_name(
        post_id: int = typer.Argument(..., help='ID рекламного поста'),
        advertiser_name: Optional[str] = typer.Option(
            None, '--value', help='Новое имя рекламодателя. '
        ),
):
    """Рекламный пост. Изменить имя рекламодателя."""

    asyncio.run(update_post_field(
        model=AdPost,
        post_id=post_id,
        field_name='advertiser_name',
        value=advertiser_name,
        success_message=f"    ✅  РЕКЛАМНЫЙ ПОСТ {post_id} :: Имя рекламодателя обновлено."
    ))


@app.command('set-advertiser-link')
def set_advertiser_link(
        post_id: int = typer.Argument(..., help='ID рекламного поста'),
        advertiser_link: Optional[str] = typer.Option(
            None, '--value', help='Новая ссылка на официальный ресурс рекламодателя. '
        ),
):
    """Рекламный пост. Изменить ссылку на официальный ресурс рекламодателя."""

    asyncio.run(update_post_field(
        model=AdPost,
        post_id=post_id,
        field_name='advertiser_link',
        value=advertiser_link,
        success_message=f"    ✅  РЕКЛАМНЫЙ ПОСТ {post_id} :: Ссылка на официальный ресурс рекламодателя изменена."
    ))


@app.command('set-title')
def set_title(
        post_id: int = typer.Argument(..., help='ID рекламного поста'),
        title: Optional[str] = typer.Option(
            None, '--value', help='Новый заголовок рекламного поста. '
        ),
):
    """Рекламный пост. Изменить заголовок поста."""

    asyncio.run(update_post_field(
        model=AdPost,
        post_id=post_id,
        field_name='title',
        value=title,
        success_message=f"    ✅  РЕКЛАМНЫЙ ПОСТ {post_id} :: Заголовок поста обновлен."
    ))


@app.command('set-text')
def set_text(
        post_id: int = typer.Argument(..., help='ID рекламного поста'),
        text: Optional[str] = typer.Option(
            None, '--value', help='Новый текст рекламного поста. '
        ),
):
    """Рекламный пост. Изменить текст поста."""

    asyncio.run(update_post_field(
        model=AdPost,
        post_id=post_id,
        field_name='text',
        value=text,
        success_message=f"    ✅  РЕКЛАМНЫЙ ПОСТ {post_id} :: Текст поста обновлен."
    ))


@app.command('set-link')
def set_link(
        post_id: int = typer.Argument(..., help='ID рекламного поста'),
        link: Optional[str] = typer.Option(
            None, '--value', help='Новая ссылка рекламного поста. '
        ),
):
    """Рекламный пост. Изменить ссылку поста."""

    asyncio.run(update_post_field(
        model=AdPost,
        post_id=post_id,
        field_name='link',
        value=link,
        success_message=f"    ✅  РЕКЛАМНЫЙ ПОСТ {post_id} :: Ссылка поста обновлена."
    ))


@app.command('set-tags')
def set_tags(
        post_id: int = typer.Argument(..., help='ID рекламного поста'),
        tags: Optional[str] = typer.Option(
            None, '--value', help='Новые тэги рекламного поста. '
                                  'Перечисление тэгов через пробел.'
        ),
):
    """Рекламный пост. Изменить тэги поста."""

    asyncio.run(update_post_field(
        model=AdPost,
        post_id=post_id,
        field_name='tags',
        value=tags,
        success_message=f"    ✅  РЕКЛАМНЫЙ ПОСТ {post_id} :: Тэги поста обновлены."
    ))


@app.command('set-dates')
def set_dates(
        post_id: int = typer.Argument(..., help='ID рекламного поста'),
        dates: Optional[str] = typer.Option(
            None, '--value', help='Новое расписание рекламного поста. '
                                  'Перечисление дат через пробел (по МСК). '
                                  'ДД.ММ.ГГГГ-ЧЧ:ММ'
        ),
):
    """Рекламный пост. Изменить расписание публикации поста."""

    asyncio.run(update_post_dates(
        model=AdPost,
        post_id=post_id,
        value=dates,
        success_message=f"    ✅  РЕКЛАМНЫЙ ПОСТ {post_id} :: Расписание поста обновлено."
    ))


@app.command('add-dates')
def add_dates(
        post_id: int = typer.Argument(..., help='ID рекламного поста'),
        dates: Optional[str] = typer.Option(
            None, '--value', help='Добавление дат в расписание рекламного поста. '
                                  'Перечисление дат через пробел (по МСК). '
                                  'ДД.ММ.ГГГГ-ЧЧ:ММ'
        ),
):
    """Рекламный пост. Добавить даты в расписание публикации поста."""

    asyncio.run(add_post_dates(
        model=AdPost,
        post_id=post_id,
        value=dates,
        success_message=f"    ✅  РЕКЛАМНЫЙ ПОСТ {post_id} :: В расписание поста добавлены новые даты."
    ))
