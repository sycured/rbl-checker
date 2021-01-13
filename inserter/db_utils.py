"""Create and return db_pool and provides function to insert result."""
from aiopg import Pool, create_pool

from config import db_host, db_name, db_pass, db_port, db_user


async def insert_result(db_pool, date, ip, rblname):
    """Insert data to the correct table."""
    insert = f'insert into rbl (date, ip_srv, rblname) ' \
             f"values ('{date}', '{ip}', '{rblname}');"
    async with db_pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute(insert)


async def create_db_pool() -> Pool:
    """Create and return pool."""
    dsn = f'postgres://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}'
    pool = await create_pool(dsn=dsn)
    return pool
