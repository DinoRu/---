from datetime import timedelta, datetime
from typing import List

from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.responses import JSONResponse

from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import RoleChecker, RefreshTokenBearer, AccessTokenBearer, get_current_user, get_user_or_404
from app.auth.schemas import UserCreateModel, UserLoginModel, UserModel, UserPartialUpdate
from app.auth.service import UserService
from app.auth.utils import verify_password, create_access_token
from app.db.main import get_session
from app.errors import UserAlreadyExists, InvalidCredentials, InvalidToken, UserNotFound, InsufficientPermission

auth_router = APIRouter()
user_service = UserService()
role_checker = RoleChecker(["admin", "user"])
admin_checker = RoleChecker(["admin"])

REFRESH_TOKEN_EXPIRY = 2

#Bearer Token

@auth_router.post("/signup", status_code=status.HTTP_201_CREATED)
async def create_user_account(
		user_data: UserCreateModel,
		session: AsyncSession = Depends(get_session)
):
	username = user_data.username
	user_exists = await user_service.user_exist(username, session)
	if user_exists:
		raise UserAlreadyExists()
	new_user = await user_service.create_user(user_data, session)

	return {
		"message": "Account created!",
		"user": new_user
	}

@auth_router.post("/login")
async def login_user(
		login_data: UserLoginModel, session: AsyncSession = Depends(get_session)
):
	username = login_data.username
	password = login_data.password

	user = await user_service.get_user_by_username(username, session)

	if user is not None:
		password_valid = verify_password(password, user.password_hash)

		if password_valid:
			access_token = create_access_token(
				user_data={
					"username": user.username,
					"user_uid": str(user.uid),
					"role": user.role,
				}
			)

			refresh_token = create_access_token(
				user_data={
					"username": user.username,
					"user_uid": str(user.uid)
				},
				refresh=True,
			)
			return JSONResponse(
				content={
					"message": "Login successful",
					"access_token": access_token,
					"refresh_token": refresh_token,
					"user": {
						"username": user.username,
						"uid": str(user.uid),
						"role": user.role
					}
				}
			)
		raise InvalidCredentials()


@auth_router.post('/admin/login')

@auth_router.get("/refresh_token")
async def get_new_access_token(token_details: dict = Depends(RefreshTokenBearer())):
	expiry_timestamp = token_details['exp']

	if datetime.fromtimestamp(expiry_timestamp) > datetime.now():
		new_access_token = create_access_token(user_data=token_details["user"])
		return JSONResponse(content={"access_token": new_access_token})

	raise InvalidToken


@auth_router.get("/me", response_model=UserModel)
async def get_current_user(
		user = Depends(get_current_user),
		_: bool = Depends(AccessTokenBearer)
):
	return user

@auth_router.get("/users", response_model=List[UserModel], status_code=status.HTTP_200_OK)
async def get_all_users(
		session: AsyncSession = Depends(get_session),
):
	users = await user_service.get_all_users(session)
	return users


@auth_router.get("/users/{user_id}", status_code=status.HTTP_200_OK, response_model=UserModel)
async def get_user(
		user = Depends(get_user_or_404),
		session: AsyncSession = Depends(get_session)
):
	return user


@auth_router.patch("/update/{user_id}", status_code=status.HTTP_200_OK)
async def update_user(
		update_data: UserPartialUpdate,
		user = Depends(get_user_or_404),
		session: AsyncSession = Depends(get_session)
):
	user_updated = await user_service.update_user(user, update_data, session)
	return user_updated

@auth_router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_user(
		user_to_delete = Depends(get_user_or_404),
		user = Depends(get_current_user),
		session: AsyncSession = Depends(get_session),
		_: bool = Depends(AccessTokenBearer)
):
	if user.role == 'admin':
		await session.delete(user_to_delete)
		await session.commit()
	else :
		raise HTTPException(
		status_code=status.HTTP_401_UNAUTHORIZED,
		detail="Insufficient permissions"
	)


