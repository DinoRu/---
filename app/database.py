from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from app.config import settings

engine = create_async_engine(settings.active_database_url())
async_session_maker = async_sessionmaker(bind=engine, expire_on_commit=False)

Base = declarative_base()


async def get_session():
	async with async_session_maker() as session:
		yield session