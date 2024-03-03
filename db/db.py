import asyncpg
from asyncpg import Pool

DB_USER = 'postgres_yt1'
DB_PASSWORD = 'postgres_yt1'
DB_NAME = 'postgres_yt1'
DB_HOST = 'localhost'


async def create_conn():
    try:
        return await asyncpg.create_pool(f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:5492/{DB_NAME}', max_size=200)
    except Exception as error:
        print("Ошибка при создании пула соединений:", error)


async def db_start(pool: Pool) -> None:
    try:
        async with pool.acquire() as conn:
            await conn.execute('CREATE TABLE IF NOT EXISTS products (id SERIAL PRIMARY KEY, arcticle INTEGER UNIQUE NOT NULL, youtube_url TEXT)')
    except Exception as e:
        print(f"Error creating table: {e}")


async def set_product(pool: Pool, article_id: int, youtube_url: str | None) -> None:
    try:
        async with pool.acquire() as conn:
            await conn.execute('INSERT INTO products (arcticle, youtube_url) VALUES ($1, $2)', article_id, youtube_url)
    except Exception as e:
        print(f"Error set product: {e}")


async def get_product(pool: Pool, article_id: int) -> tuple[int, str] | None:
    try:
        async with pool.acquire() as conn:
            return await conn.fetchrow('SELECT arcticle, youtube_url FROM products WHERE arcticle = $1', article_id)
    except Exception as e:
        print(f"Error get product: {e}")


async def update_product(pool: Pool, article_id: int, youtube_url: str) -> None:
    try:
        async with pool.acquire() as conn:
            await conn.execute('UPDATE products SET youtube_url = $1 WHERE arcticle = $2', youtube_url, article_id)
    except Exception as e:
        print(f"Error update product: {e}")


async def get_products(pool: Pool) -> list[tuple[int, str]]:
    try:
        async with pool.acquire() as conn:
            return await conn.fetch('SELECT arcticle, youtube_url FROM products')
    except Exception as e:
        print(f"Error get products: {e}")


async def delete_product(pool: Pool, article_id: int) -> None:
    try:
        async with pool.acquire() as conn:
            await conn.execute('DELETE FROM products WHERE arcticle = $1', article_id)
    except Exception as e:
        print(f"Error delete product: {e}")
