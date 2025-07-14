from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import sessionmaker
from app.models import Base, User
import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./test.db")
engine = create_async_engine(DATABASE_URL, echo=False, future=True)
async_session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

async def get_async_session():
    async with async_session() as session:
        yield session

class UserRepository:
    def __init__(self, session):
        self.session = session

    async def get_by_username(self, username):
        result = await self.session.execute(
            User.__table__.select().where(User.username == username)
        )
        user = result.fetchone()
        return user and User(**dict(user))

    async def create_user(self, username, password, role):
        new_user = User(username=username, password=password, role=role)
        self.session.add(new_user)
        await self.session.commit()
        await self.session.refresh(new_user)
        return new_user

    async def update_user(self, user_id, new_password):
        result = await self.session.execute(
            User.__table__.select().where(User.id == user_id)
        )
        user_row = result.fetchone()
        if not user_row:
            return None
        await self.session.execute(
            User.__table__.update().where(User.id == user_id).values(password=new_password)
        )
        await self.session.commit()
        updated = await self.session.execute(
            User.__table__.select().where(User.id == user_id)
        )
        row = updated.fetchone()
        return row and User(**dict(row))

    async def list_users(self):
        result = await self.session.execute(User.__table__.select())
        return [User(**dict(r)) for r in result.fetchall()]

    async def delete_user(self, user_id):
        result = await self.session.execute(User.__table__.select().where(User.id == user_id))
        user = result.fetchone()
        if not user:
            return False
        await self.session.execute(User.__table__.delete().where(User.id == user_id))
        await self.session.commit()
        return True

def get_user_repository(session):
    return UserRepository(session)
