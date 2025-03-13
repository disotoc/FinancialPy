"""Funcionalidades de base datos"""
# financial_py/database.py

import os
import sqlite3
from pathlib import Path
from typing import Any, Dict, List, NamedTuple
from dotenv import load_dotenv

from financial_py import DB_READ_ERROR, DB_WRITE_ERROR, SUCCESS

ENV_PATH = os.path.join(os.path.dirname(__file__), os.pardir, ".env")
load_dotenv(dotenv_path=ENV_PATH)

DEFAULT_DB_FILE_PATH = Path(os.getenv(
    'DB_PATH',
    str(Path.home().joinpath("." + Path.home().stem + "_financial.db"))
))


def get_database_path() -> Path:
    """Return the current path to the database."""
    print(f"DB_PATH from env: {os.getenv('DB_PATH')}")
    if os.getenv('DB_PATH'):
        return Path(os.getenv('DB_PATH'))
    return DEFAULT_DB_FILE_PATH

def init_database(db_path: Path) -> int:
    """Create the SQLite database and necessary tables."""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Crear tabla para transacciones financieras
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                description TEXT NOT NULL,
                amount REAL NOT NULL,
                date TEXT NOT NULL,
                category TEXT,
                type TEXT NOT NULL
            )
        ''')
        
        conn.commit()
        conn.close()
        return SUCCESS
    except sqlite3.Error:
        return DB_WRITE_ERROR

class DBResponse(NamedTuple):
    """Response from the database."""
    transactions: List[Dict[str, Any]]
    error: int

class DatabaseHandler:
    def __init__(self, db_path: Path) -> None:
        self._db_path = db_path

    def read_transactions(self) -> DBResponse:
        try:
            conn = sqlite3.connect(self._db_path)
            cursor = conn.cursor()
            
            cursor.execute("SELECT * FROM transactions")
            rows = cursor.fetchall()
            
            transactions = []
            for row in rows:
                transactions.append({
                    "id_transaction": row[0],
                    "transaction_type": row[1],
                    "importe": row[2],
                    "transaction_date": row[3],
                })
            
            conn.close()
            return DBResponse(transactions, SUCCESS)
        except sqlite3.Error:
            return DBResponse([], DB_READ_ERROR)

    def write_transaction(self, transaction: Dict[str, Any]) -> DBResponse:
        try:
            conn = sqlite3.connect(self._db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO transactions (description, amount, date, category, type)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                transaction["description"],
                transaction["amount"],
                transaction["date"],
                transaction["category"],
                transaction["type"]
            ))
            
            conn.commit()
            conn.close()
            return DBResponse([transaction], SUCCESS)
        except sqlite3.Error:
            return DBResponse([transaction], DB_WRITE_ERROR)

if __name__ == "__main__":
    db_path = get_database_path()
    print(f"DB Path: {db_path}")
