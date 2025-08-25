import asyncio
import typer
from typing import Optional
from pathlib import Path
from src.database import AsyncSessionLocal
from src.models import Post
from .utils import post_activity_toggle, update_post_field, parse_filename


app = typer.Typer()


async def add_single_post(photo_file: str, author: str) -> bool:
    """Добавляет один пост с парсингом метаданных из имени файла"""
    try:
        # Парсим имя файла
        metadata = parse_filename(photo_file)

        # Формируем относительный путь
        author_dir = author.replace(' ', '_')
        relative_path = f"@/{author_dir}/{photo_file}"

        async with AsyncSessionLocal() as db:
            db.add(Post(
                photo_path=relative_path,
                title=metadata['title'] or photo_file.stem.replace('_', ' ').title(),
                author=author,
                location=metadata['location'],
                date=metadata['date'],
                tags=metadata['tags'],
                is_active=True,
                shown=False
            ))
            await db.commit()

        return True

    except Exception as e:
        typer.secho(f"  ❌  Ошибка обработки {photo_file}: {e}", fg=typer.colors.RED)
        return False


@app.command("mass-add")
def bulk_add_from_folder(
        folder: Path = typer.Option(..., "--folder", help="Папка с фотографиями"),
        author: str = typer.Option(..., "--author", help="Автор фотографий")
):
    """Добавить все фото из папки с автоматическим парсингом метаданных"""

    async def _process_folder():
        success_count = 0
        error_count = 0

        # Ищем все jpg и png файлы
        for photo_file in list(folder.glob("*.jpg")) + list(folder.glob("*.png")):
            try:
                if await add_single_post(photo_file.name, author):
                    success_count += 1
                    typer.secho(f"    ✅  Добавлен: {photo_file.name}", fg=typer.colors.GREEN)
                else:
                    error_count += 1
            except Exception as e:
                error_count += 1
                typer.secho(f"  ❌ Ошибка с {photo_file.name}: {e}", fg=typer.colors.RED)

        typer.secho(f"\n    📊  Итог: Успешно {success_count}, Ошибок {error_count}", fg=typer.colors.BLUE)

    asyncio.run(_process_folder())


@app.command("add")
def add_post(
        file: Path = typer.Option(..., "--file"),
        title: str = typer.Option(None, "--title"),
        author: str = typer.Option(None, "--author"),
        date: str = typer.Option(None, "--date"),
        location: str = typer.Option(None, "--location"),
        caption: str = typer.Option(None, "--caption"),
        header: str = typer.Option(None, "--header"),
        tags: str = typer.Option(None, "--tags", help='Перечисление тэгов через пробел, '
                                                      'e.g. "nature sunset photo_art"'),
        active: bool = typer.Option(True, "--active/--no-active"),
):
    async def _add():
        async with AsyncSessionLocal() as db:
            db.add(Post(
                photo_path=str(file.resolve()),
                title=title,
                author=author,
                date=date,
                location=location,
                caption=caption,
                header=header,
                tags=tags,
                is_active=active,
            ))
            await db.commit()

    asyncio.run(_add())
    typer.echo("    ✅  Регулярный Пост добавлен")


@app.command("activate")
def activate_post(post_id: int):
    """Регулярный пост. Изменить статус на активный."""

    try:
        result = asyncio.run(post_activity_toggle(
            model=Post,
            post_id=post_id,
            active_status=True)
        )
        if result:
            typer.secho(f"    ✅  Регулярный Пост id={post_id} активирован", fg=typer.colors.GREEN)

    except Exception as e:
        typer.secho(
            f"    ❌  При попытке смены статуса is_active "
            f"Регулярного Поста id={post_id} произошла непредвиденная ошибка\n"
            f"{e}",
            fg=typer.colors.RED
        )


@app.command("deactivate")
def deactivate_post(post_id: int):
    """Регулярный пост. Изменить статус на неактивный."""
    try:
        result = asyncio.run(post_activity_toggle(
            model=Post,
            post_id=post_id,
            active_status=False)
        )
        if result:
            typer.secho(f"    ✅  Регулярный Пост id={post_id} деактивирован", fg=typer.colors.GREEN)

    except Exception as e:
        typer.secho(
            f"    ❌  При попытке смены статуса is_active "
            f"Регулярного Поста id={post_id} произошла непредвиденная ошибка\n"
            f"{e}",
            fg=typer.colors.RED
        )


@app.command('set-photo-path')
def set_title(
        post_id: int = typer.Argument(..., help='ID регулярного поста'),
        photo_path: Optional[str] = typer.Option(
            None, '--value', help='Новый файл поста. '
        ),
):
    """Регулярный пост. Изменить путь до фото-файла."""

    asyncio.run(update_post_field(
        model=Post,
        post_id=post_id,
        field_name='photo_path',
        value=photo_path,
        success_message=f"    ✅  РЕГУЛЯРНЫЙ ПОСТ {post_id} :: Путь до фото-файла обновлен."
    ))


@app.command('set-title')
def set_title(
        post_id: int = typer.Argument(..., help='ID регулярного поста'),
        title: Optional[str] = typer.Option(
            None, '--value', help='Новое название снимка. '
                                  'Отсутствие аргумента - удаление названия снимка.'
        ),
):
    """Регулярный пост. Изменить название снимка."""

    asyncio.run(update_post_field(
        model=Post,
        post_id=post_id,
        field_name='title',
        value=title,
        success_message=f"    ✅  РЕГУЛЯРНЫЙ ПОСТ {post_id} :: Название снимка обновлено."
    ))


@app.command('set-author')
def set_author(
        post_id: int = typer.Argument(..., help='ID регулярного поста'),
        author: Optional[str] = typer.Option(
            None, '--value', help='Новый автор снимка. '
                                  'Отсутствие аргумента - удаление автора снимка.'
        )
):
    """Регулярный пост. Изменить автора снимка."""

    asyncio.run(update_post_field(
        model=Post,
        post_id=post_id,
        field_name='author',
        value=author,
        success_message=f"    ✅  РЕГУЛЯРНЫЙ ПОСТ {post_id} :: Автор снимка обновлен."
    ))


@app.command('set-date')
def set_date(
        post_id: int = typer.Argument(..., help='ID регулярного поста'),
        date: Optional[str] = typer.Option(
            None, '--value', help='Новая дата снимка. '
                                  'Отсутствие аргумента - удаление даты снимка'
        )
):
    """Регулярный пост. Изменить дату снимка."""
    asyncio.run(update_post_field(
        model=Post,
        post_id=post_id,
        field_name='date',
        value=date,
        success_message=f"    ✅  РЕГУЛЯРНЫЙ ПОСТ {post_id} :: Дата снимка обновлена."
    ))


@app.command('set-location')
def set_location(
        post_id: int = typer.Argument(..., help='ID регулярного поста'),
        location: Optional[str] = typer.Option(
            None, '--value', help='Новая локация снимка. '
                                  'Отсутствие аргумента - удаление локации снимка.'
        )
):
    """Регулярный пост. Изменить локацию снимка."""
    asyncio.run(update_post_field(
        model=Post,
        post_id=post_id,
        field_name='location',
        value=location,
        success_message=f"    ✅  РЕГУЛЯРНЫЙ ПОСТ {post_id} :: Локация снимка обновлена."
    ))


@app.command('set-caption')
def set_caption(
        post_id: int = typer.Argument(..., help='ID регулярного поста'),
        caption: Optional[str] = typer.Option(
            None, '--value', help='Новое описание снимка. '
                                  'Отсутствие аргумента - удаление описания снимка.'
        )
):
    """Регулярный пост. Изменить описание снимка."""
    asyncio.run(update_post_field(
        model=Post,
        post_id=post_id,
        field_name='caption',
        value=caption,
        success_message=f"    ✅  РЕГУЛЯРНЫЙ ПОСТ {post_id} :: Описание снимка обновлено."
    ))


@app.command('set-header')
def set_header(
        post_id: int = typer.Argument(..., help='ID регулярного поста'),
        header: Optional[str] = typer.Option(
            None, '--value', help='Новый заголовок поста. '
                                  'Отсутствие аргумента - удаление заголовка поста.'
        )
):
    """Регулярный пост. Изменить заголовок поста."""
    asyncio.run(update_post_field(
        model=Post,
        post_id=post_id,
        field_name='header',
        value=header,
        success_message=f"    ✅  РЕГУЛЯРНЫЙ ПОСТ {post_id} :: Заголовок поста обновлен."
    ))


@app.command('set-tags')
def set_tags(
        post_id: int = typer.Argument(..., help='ID регулярного поста'),
        tags: Optional[str] = typer.Option(
            None, '--value', help='Новые тэги поста. '
                                  'Перечислять тэги необходимо через пробел. '
                                  'Отсутствие аргумента - удаление тэгов поста.'
        )
):
    """Регулярный пост. Изменить заголовок поста."""
    asyncio.run(update_post_field(
        model=Post,
        post_id=post_id,
        field_name='tags',
        value=tags,
        success_message=f"    ✅  РЕГУЛЯРНЫЙ ПОСТ {post_id} :: Тэги поста обновлены."
    ))
