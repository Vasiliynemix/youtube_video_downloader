import sqlite3

DB_FILE = 'database.db'


# async def create_conn():
#     try:
#         return await aiosqlite.connect(DB_FILE)
#     except Exception as error:
#         print("Ошибка при создании соединения:", error)


def db_start(connection) -> None:
    try:
        with sqlite3.connect(DB_FILE, timeout=15000) as data:
            curs = data.cursor()
            curs.execute('CREATE TABLE IF NOT EXISTS products (article INTEGER UNIQUE NOT NULL, youtube_url TEXT)')
    except Exception as e:
        print(f"Ошибка при создании таблицы: {e}")


def set_product(connection, article_id: int, youtube_url) -> None:
    try:
        with sqlite3.connect(DB_FILE, timeout=15000) as data:
            curs = data.cursor()
            curs.execute('INSERT INTO products (article, youtube_url) VALUES (?, ?)', (article_id, youtube_url))
    except Exception as e:
        print(f"Ошибка при добавлении продукта: {e}")


def get_product(connection, article_id: int):
    try:
        with sqlite3.connect(DB_FILE, timeout=15000) as data:
            curs = data.cursor()
            curs.execute('SELECT article, youtube_url FROM products WHERE article = ?', (article_id,))
            return curs.fetchone()
    except Exception as e:
        print(f"Ошибка при получении продукта: {e}")


def update_product(connection, article_id: int, youtube_url: str) -> None:
    try:
        with sqlite3.connect(DB_FILE, timeout=15000) as data:
            curs = data.cursor()
            curs.execute('UPDATE products SET youtube_url = ? WHERE article = ?', (youtube_url, article_id))
    except Exception as e:
        print(f"Ошибка при обновлении продукта: {e}")