import uuid
from typing import List

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.users import User
from app.repositories.users import user_repository, hsh_pwd
from app.schemas.users import UserOut, ChangePasswordRequest, CreateUserRequest, LoginData, \
	TokenData
from app.utils.jwt_handler import create_access_token


class UserController:

	@classmethod
	async def add_user(cls,
					   session: AsyncSession,
					   user_data: CreateUserRequest
					   ) -> User:
		user = await user_repository.create(
			session=session,
			data=user_data
		)
		if not user:
			raise HTTPException(
				status_code=status.HTTP_400_BAD_REQUEST,
				detail="Invalid data passed."
			)
		return user

	@classmethod
	async def all_users(cls, session: AsyncSession) -> List[UserOut]:
		users = await user_repository.get_users(session=session)
		if not users:
			raise HTTPException(
				status_code=status.HTTP_404_NOT_FOUND,
				detail="List of users not found."
			)
		return users

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

	@classmethod
	async def change_password_user(cls, session: AsyncSession,
								   user_id: uuid.UUID, data: ChangePasswordRequest):
		return await user_repository.change_user_password(
			session=session,
			user_id=user_id,
			data=data
		)

	@classmethod
	async def get_user_by_username(cls, session: AsyncSession, username: str) -> UserOut:
		user = await user_repository.get_user_by_username(session, username)
		if not user:
			raise HTTPException(
				status_code=status.HTTP_404_NOT_FOUND,
				detail="User not found."
			)
		return user

	@classmethod
	async def login(cls, username: str, password: str, session: AsyncSession) -> TokenData:
		user = await user_repository.get_user_by_username(session=session,
														  username=username)
		if not user:
			raise HTTPException(
				status_code=status.HTTP_404_NOT_FOUND,
				detail="User not found."
			)
		if not hsh_pwd.verify_hash(password, user.password):
			raise HTTPException(
				status_code=status.HTTP_401_UNAUTHORIZED,
				detail="Incorrect password"
			)
		token = create_access_token(user={
			"user_id": str(user.user_id),
			"username": user.username
		})
		return TokenData(access_token=token, token_type='bearer')



user_controller = UserController()