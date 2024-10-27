import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from sqlalchemy import Table, MetaData, Column, String, Integer, ForeignKey

metadata = MetaData()

# Определение таблицы
users_table = Table(
    'users',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String),
)

friendship_table = Table(
    'friendships',
    metadata,
    Column('user_id', ForeignKey("users.id")),
    Column('friend_id', ForeignKey("users.id")),
)

DATABASE_URL = "sqlite+aiosqlite:///example.db"
engine = create_async_engine(DATABASE_URL, echo=True)

async_session = async_sessionmaker(engine, expire_on_commit=True)


async def create_tables():
    async with engine.begin() as conn:
        # Создаем все таблицы, определенные в metadata
        await conn.run_sync(metadata.create_all)


async def async_main() -> None:

    async with async_session() as session:
        # q = users_table.insert().values(id=3423432, name="John").returning(users_table)
        q = users_table.select()
        res = await session.execute(q)
        print(res.fetchall())
        await session.commit()

if __name__ == '__main__':
    asyncio.run(async_main())
