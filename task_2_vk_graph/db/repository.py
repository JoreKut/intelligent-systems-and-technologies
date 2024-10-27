"""
    - users
        + user_id (PK)
        + name

    - friendship
        + user_id (FK) --> users.user_id
        + friend_id (FK) --> users.user_id
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine

engine = create_async_engine("sqlite+aiosqlite://example.db", echo=True)

from pydantic import BaseModel


class UserCreateData(BaseModel):
    user_id: str
    name: str = "undefined"


class UserUpdateData(UserCreateData):
    ...


class BaseRepository:

    def __init__(self, conn):
        self.conn = conn


class UserRepository(BaseRepository):


    async def create(self, data: UserCreateData):
        q = """
            insert into users('user_id', 'name')
            values (%(user_id)s, %(name)s)
        """ % {
            "user_id": data.user_id,
            "name": data.name,
        }
        self.conn.execute(q)

    async def read(self, id_):
        q = """
            select u.user_id, u.name
            from users 
            where u.user_id = %(id)s
        """ % {
            "id": id_
        }

        self.conn.execute(q)

    async def read_all(self, limit):
        q = """
            select u.user_id, u.name
            from users 
            where u.user_id = %(id)s
        """
        self.conn.execute(q)

    async def update(self, data: UserUpdateData):
        q = """
            update users u
            set u.name=%(name)s)
            where u.user_id = %(user_id)s
        """ % {
            "user_id": data.user_id,
            "name": data.name,
        }
        self.conn.execute(q)

    async def delete(self, id_):
        q = """
            delete from users u
            where u.user_id = %(user_id)s
        """ % {
            "user_id": id_
        }
        self.conn.execute(q)


class CreateFriendshipData(BaseModel):
    user_id: str
    friend_ids: list[str] = []



class FriendshipRepository(BaseRepository):

    async def create(self, data: CreateFriendshipData):
        values = []
        for friend_id in data.friend_ids:
            values.append(
                "(%(user_id)s, %(friend_id)s)" % {"user_id": data.user_id, "friend_id": friend_id}
            )

        values_str = ",".join(values)
        q = f"""
            insert into friendship('user_id', 'friend_id')
            values {values_str}
        """

        self.conn.execute(q)

    async def read(self, user_id):
        q = """
            select f.user_id, array_agg(f.friend_id)
            from friendship f
            where id = %(user_id)s
            group by f.user_id
        """ % {"user_id": user_id}

        self.conn.execute(q)

    async def update(self):
        pass

    async def delete(self):
        pass
