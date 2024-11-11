import uuid

from sqlalchemy import select, update, delete
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.users import User
from app.schemas.users import ChangePasswordRequest, CreateUserRequest
from app.utils.hash_password import HashPassword

hsh_pwd = HashPassword()

class UserRepository:

	@classmethod
	async def create(cls, session: AsyncSession, data: CreateUserRequest) -> User:
		new_user = User(**data.dict())
		hashed_password = hsh_pwd.create_hash(new_user.password)
		new_user.password = hashed_password
		try:
			session.add(new_user)
			await session.commit()
			await session.refresh(new_user)
		except SQLAlchemyError as e:
			# Rollback en cas d'erreur
			await session.rollback()
		return new_user

	@classmethod
	async def get_users(cls, session: AsyncSession):
		query = select(User)
		result = await session.execute(query)
		return result.scalars().all()

	@classmethod
	async def get_user(cls, session: AsyncSession, user_id: uuid.UUID):
		stmt = select(User).where(User.user_id == user_id)
		result = await session.execute(stmt)
		return result.scalar_one_or_none()

	@classmethod
	async def get_user_by_username(cls, session: AsyncSession, username: str):
		stmt = select(User).where(User.username == username)
		result = await session.execute(stmt)
		return result.scalar_one_or_none()

	@classmethod
	async def update(cls,
					 session: AsyncSession,
					 user_id: uuid.UUID,
					 full_name: str = None) -> bool:
		stmt = (
			update(User)
			.where(User.user_id == user_id)
			.values(full_name=full_name)
			.execution_options(synchronize_session='fetch')
		)
		result = await session.execute(stmt)
		await session.commit()
		return result.rowcount > 0

	@classmethod
	async def delete(cls, user_id: uuid.UUID, session: AsyncSession) -> bool:
		stmt = delete(User).where(User.user_id == user_id)
		result = await session.execute(stmt)
		await session.commit()
		return result.rowcount > 0

	@classmethod
	async def delete_users(cls, session: AsyncSession) -> bool:
		stmt = delete(User)
		result = await session.execute(stmt)
		await session.commit()
		return result.rowcount > 0

	@classmethod
	async def change_user_password(cls, session: AsyncSession, data: ChangePasswordRequest,
								   user_id: uuid.UUID):
		user = await cls.get_user(session, user_id)
		if not hsh_pwd.verify_hash(data.old_password, user.password):
			raise ValueError(
				f"Old password provided doesn't match, please try again")
		user.password = hsh_pwd.create_hash(data.new_password)
		await session.commit()


user_repository = UserRepository()