import uuid
from typing import List

from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.controllers.users import user_controller
from app.database import get_session
from app.schemas.users import CreateUserRequest, UpdateUserRequest, ChangePasswordRequest, UserOut, \
	TokenData

router = APIRouter(
	prefix='/users',
	tags=['Users'],
	responses={404: {"description": "Not found."}}
)

# Get all users
@router.get("/all", status_code=status.HTTP_200_OK, summary="Get all users", response_model=List[UserOut])
async def list_users(session: AsyncSession = Depends(get_session)):
	users = await user_controller.all_users(session)
	return users


# Get user by ID
@router.get('/user/{user_id}', status_code=status.HTTP_200_OK, summary="Get user by ID")
async def get_user(
		user_id: uuid.UUID,
		session: AsyncSession = Depends(get_session)
):
	return await user_controller.get_user_by_id(session, user_id)


# Create or Add new user
@router.post("/add",
			 status_code=status.HTTP_201_CREATED,
			 response_model=UserOut,
			 summary="Add new user")
async def add_user(
		user_data: CreateUserRequest,
		session: AsyncSession = Depends(get_session)
):
	return await user_controller.add_user(
		session=session,
		user_data=user_data
	)

# Update user by ID
@router.patch("/user/{user_id}",
			  status_code=status.HTTP_200_OK,
			  summary="Update user name")
async def modify_user_name(
		user_id: uuid.UUID,
		request: UpdateUserRequest,
		session: AsyncSession = Depends(get_session)
):
	return await user_controller.update_user(
		session=session,
		user_id=user_id,
		full_name=request.full_name
	)

# Change Password
@router.patch("/change_password/{user_id}",
			 status_code=status.HTTP_201_CREATED,
			 summary="Update user password")
async def change_password(
		user_id: uuid.UUID,
		request: ChangePasswordRequest,
		session: AsyncSession = Depends(get_session)
):
	"""
	Change password for logged user
	:param user_id:
	:param request:
	:param session:
	:return: dict()
	"""
	try:
		await user_controller.change_password_user(
			session=session,
			user_id=user_id,
			data=request
		)
		return {"result": 'Password changed successfully.'}
	except ValueError as e:
		raise HTTPException(
			status_code=400, detail=f"{e}")
	except Exception as e:
		raise HTTPException(
			status_code=500,
			detail=f"An unexpected error occurred. Report this message to support: {e}")

# Delete user
@router.delete("/user/{user_id}", status_code=status.HTTP_200_OK, summary="Delete user")
async def remove_user(
		user_id: uuid.UUID,
		session: AsyncSession = Depends(get_session)
):
	return await user_controller.delete_user(session=session, user_id=user_id)

# Delete all user
@router.delete("/remove/users", status_code=status.HTTP_200_OK, summary="Remove all users")
async def remove_users(session: AsyncSession = Depends(get_session)):
	return await user_controller.delete_all_users(session)


@router.post("/login", status_code=status.HTTP_201_CREATED, response_model=TokenData)
async def login(
		form_data: OAuth2PasswordRequestForm = Depends(),
		session: AsyncSession = Depends(get_session)
):
	return await user_controller.login(username=form_data.username,
									   password=form_data.password,
									   session=session)
