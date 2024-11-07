import uuid

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.users import user_repository
from app.schemas.users import UserOut


class UserController:

	@classmethod
	async def add_user(cls,
					   session: AsyncSession,
					   full_name: str,
					   password: str
					   ):
		user = await user_repository.create(
			session=session,
			full_name=full_name,
			password=password
		)
		if not user:
			raise HTTPException(
				status_code=status.HTTP_400_BAD_REQUEST,
				detail="Invalid data passed."
			)
		return {
			"user_id": user.user_id,
			"full_name": full_name,
		}

	@classmethod
	async def all_users(cls, session: AsyncSession):
		users = await user_repository.get_users(session=session)
		if not users:
			raise HTTPException(
				status_code=status.HTTP_404_NOT_FOUND,
				detail="List of users not found."
			)
		return [{'user_id': user.user_id, 'full_name': user.full_name} for user in users]

	# Get user by user_id
	@classmethod
	async def get_user_by_id(cls, session: AsyncSession, user_id: uuid.UUID) -> UserOut:
		user = await user_repository.get_user(session, user_id)
		if not user:
			raise HTTPException(
				status_code=status.HTTP_404_NOT_FOUND,
				detail="User not found."
			)
		return UserOut.from_orm(user)

	@classmethod
	async def update_user(
			cls,
			session: AsyncSession,
			user_id: uuid.UUID,
			full_name: str
	):
		success = await user_repository.update(
			session=session,
			full_name=full_name,
			user_id=user_id
		)
		if not success:
			raise HTTPException(
				status_code=status.HTTP_400_BAD_REQUEST,
				detail="User not found or bad request data."
			)
		return {'detail': "User udpated successfully."}

	@classmethod
	async def delete_user(cls, session: AsyncSession, user_id: uuid.UUID):
		success = await user_repository.delete(session=session, user_id=user_id)
		if not success:
			raise HTTPException(
				status_code=status.HTTP_404_NOT_FOUND,
				detail="User not found."
			)
		return {'detail': "User deleted successfully."}


	@classmethod
	async def delete_all_users(cls, session: AsyncSession):
		success = await user_repository.delete_users(session=session)
		if not success:
			raise HTTPException(
				status_code=status.HTTP_400_BAD_REQUEST,
				detail="Table was empty."
			)
		return {"detail": "Users deleted successfully."}


user_controller = UserController()