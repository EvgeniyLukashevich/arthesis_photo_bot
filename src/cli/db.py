import shutil
from typing import Optional
import asyncio
import typer
from pathlib import Path
from src.database import Base, engine
from datetime import datetime
from src.core import Config

app = typer.Typer()

BACKUP_DIR = Path(Config.BASE_DIR) / "backups"
BACKUP_DIR.mkdir(exist_ok=True)


# ---------- Database ----------

@app.command("init")
def init_db():
    """Создать все таблицы в БД."""

    async def _init():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    asyncio.run(_init())
    typer.echo("✅ Таблицы созданы")


@app.command("backup")
def backup_db(
        name: Optional[str] = typer.Option(None, "--name", help="Имя файла бэкапа"),
        compress: bool = typer.Option(True, "--compress/--no-compress", help="Создать .zip архив")
):
    """Создать бэкап БД."""
    try:
        db_file = Path(Config.DB_URL.replace("sqlite+aiosqlite:///", ""))
        if not db_file.exists():
            typer.secho("❌ Файл БД не найден!", fg=typer.colors.RED)
            raise typer.Exit(1)

        timestamp = datetime.now().strftime("%d-%m-%Y_%H-%M")
        backup_name = f"{name or 'backup'}_{timestamp}.db"
        backup_path = BACKUP_DIR / backup_name

        shutil.copy2(db_file, backup_path)
        typer.echo(f"✅ Бэкап создан: {backup_path}")

        if compress:
            zip_path = backup_path.with_suffix(".zip")
            shutil.make_archive(str(zip_path.with_suffix("")), 'zip', BACKUP_DIR, backup_name)
            backup_path.unlink()
            typer.echo(f"📦 Создан архив: {zip_path}")

    except Exception as e:
        typer.secho(f"❌ Ошибка: {e}", fg=typer.colors.RED)
        raise typer.Exit(1)


@app.command("backups-list")
def list_backups():
    """Показать все бэкапы."""
    backups = sorted(BACKUP_DIR.glob("*.zip" if BACKUP_DIR.glob("*.zip") else "*.db"))
    if not backups:
        typer.echo("ℹ️ Нет бэкапов.")
        return

    typer.echo("📂 Бэкапы:")
    for i, file in enumerate(backups, 1):
        typer.echo(f"  {i}. {file.name} ({file.stat().st_size / 1024:.1f} KB)")