"""Módulo encargado del cli"""
# financial_py/cli.py

from pathlib import Path
from typing import List, Optional

import typer

from financial_py import ERRORS, __app_name__, __version__, config, database, financial_py

app = typer.Typer()

def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"{__app_name__} v{__version__}")
        raise typer.Exit()


@app.callback()
def main(
        version: Optional[bool] = typer.Option(
            None,
            "--version",
            "-v",
            help="Show the application's version and exit.",
            callback=_version_callback,
            is_eager=True,
        )
) -> None:
    return

@app.command(name="all_transactions")
def get_transactions() -> None:
    """Get all transactions."""
    db_path = database.get_database_path()
    db_handler = database.DatabaseHandler(db_path)
    response = db_handler.read_transactions()

    # Corregir esta línea
    # Mostrar las transacciones
    if not response.transactions:
        typer.echo("No hay transacciones registradas.")
    else:
        for transaction in response.transactions:
            typer.echo(transaction)
