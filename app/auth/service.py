from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.auth.schemas import UserCreateModel
from app.auth.utils import generate_passwd_hash
from app.db.models import User


class UserService:
	async def get_user_by_username(self, username: str, session: AsyncSession):
		statement = select(User).where(User.username == username)
		result = await session.execute(statement)
		user = result.scalar_one_or_none()
		return user

	async def user_exist(self, username: str, session: AsyncSession):
		user = await self.get_user_by_username(username, session)
		return True if user is not None else False

	async def create_user(self, user_data: UserCreateModel, session: AsyncSession):
		user_data_dict = user_data.model_dump()
		new_user = User(**user_data_dict)
		new_user.password_hash = generate_passwd_hash(user_data_dict["password"])
		new_user.role = "user"
		session.add(new_user)
		await session.commit()
		return new_user

	async def update_user(self, user: User, user_data: dict, session: AsyncSession):
		for k, v in user_data.items():
			setattr(user, k, v)
		await session.commit()

		return user

	async def delete(self, username: str, session: AsyncSession):
		user = await self.get_user_by_username(username, session)
		if user:
			await session.delete(user)
			await session.commit()
			return True
		return False

	async def delete_all_users(self, session: AsyncSession):
		await session.execute(delete(User))
		await session.commit()

