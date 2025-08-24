import typer
from .db import app as db_app
from .posts import app as posts_app
from .ads import app as ads_app
from .instants import app as instants_app

app = typer.Typer()

app.add_typer(db_app, name="db", help="Управление Базой Данных")
app.add_typer(posts_app, name="post", help="Управление регулярными постами")
app.add_typer(ads_app, name="ad", help="Управление рекламными постами")
app.add_typer(instants_app, name="instant", help="Управление внеочередными постами")
