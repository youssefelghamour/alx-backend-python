import asyncio
import aiosqlite


async def async_fetch_users():
    """Asynchrounous function to fetch all users from the database"""
    async with aiosqlite.connect('users.db') as db:
        async with db.execute('SELECT * FROM users') as cursor:
            users = await cursor.fetchall()
            return users

async def async_fetch_older_users():
    """Asynchronous function to fetch users older than 40 from the database"""
    async with aiosqlite.connect('users.db') as db:
        async with db.execute('SELECT * FROM users WHERE age > 40') as cursor:
            older_users = await cursor.fetchall()
            return older_users

async def fetch_concurrently():
    """Execute both function concurrently"""
    users = await asyncio.gather(async_fetch_users(), async_fetch_older_users())
    return users


if __name__ == "__main__":
    all_users, older_users = asyncio.run(fetch_concurrently())
    print("Number of all Users:", len(all_users))
    print("Number of Users older than 40:", len(older_users))