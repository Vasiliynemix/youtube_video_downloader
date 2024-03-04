import asyncpg
from asyncpg import Pool
import sqlite3
import aiosqlite

DB_USER = 'postgres_yt1'
DB_PASSWORD = 'postgres_yt1'
DB_NAME = 'postgres_yt1'
DB_HOST = 'localhost'

DB_FILE = 'database.db'


async def create_conn():
    try:
        return await aiosqlite.connect(DB_FILE)
    except Exception as error:
        print("Ошибка при создании пула соединений:", error)
        print("Ошибка при создании соединения:", error)


async def db_start(connection) -> None:
    try:
        with sqlite3.connect(DB_FILE, timeout=15000) as data:
            curs = data.cursor()
            curs.execute('CREATE TABLE IF NOT EXISTS products (article INTEGER UNIQUE NOT NULL, youtube_url TEXT)')
    except Exception as e:
        print(f"Error creating table: {e}")
        print(f"Ошибка при создании таблицы: {e}")


async def set_product(connection, article_id: int, youtube_url: str | None) -> None:
    try:
        with sqlite3.connect(DB_FILE, timeout=15000) as data:
            curs = data.cursor()
            curs.execute('INSERT INTO products (article, youtube_url) VALUES (?, ?)', (article_id, youtube_url))
    except Exception as e:
        print(f"Error set product: {e}")
        print(f"Ошибка при добавлении продукта: {e}")


async def get_product(connection, article_id: int) -> tuple[int, str] | None:
    try:
        with sqlite3.connect(DB_FILE, timeout=15000) as data:
            curs = data.cursor()
            curs.execute('SELECT article, youtube_url FROM products WHERE article = ?', (article_id,))
            return curs.fetchone()
    except Exception as e:
        print(f"Error get product: {e}")
        print(f"Ошибка при получении продукта: {e}")


async def update_product(connection, article_id: int, youtube_url: str) -> None:
    try:
        with sqlite3.connect(DB_FILE, timeout=15000) as data:
            curs = data.cursor()
            curs.execute('UPDATE products SET youtube_url = ? WHERE article = ?', (youtube_url, article_id))
    except Exception as e:
        print(f"Error update product: {e}")
        print(f"Ошибка при обновлении продукта: {e}")
