from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from app.config import settings

engine = create_async_engine(settings.active_database_url())
Async_session_maker = async_sessionmaker(bind=engine, expire_on_commit=False)

async def get_session():
	async with Async_session_maker() as session:
		yield session