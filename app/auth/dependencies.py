from typing import List, Any

from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Request, Depends
from sqlalchemy import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.auth.service import UserService
from app.auth.utils import decode_token
from app.db.main import get_session
from app.db.models import User
from app.errors import InvalidToken, AccessTokenRequired, RefreshTokenRequired, UserNotFound, InsufficientPermission

user_service = UserService()

class TokenBearer(HTTPBearer):
	def __init__(self, auto_error=True):
		super().__init__(auto_error=auto_error)

	async def __call__(self, request: Request) -> HTTPAuthorizationCredentials | None:
		creds = await super().__call__(request)

		token = creds.credentials
		token_data = decode_token(token)

		if not self.token_valid(token):
			raise InvalidToken()

		self.verify_token_data(token_data)

		return token_data

	def token_valid(self, token: str) -> bool:
		try:
			token_data = decode_token(token)

			return token_data is not None
		except Exception:
			return False

	def verify_token_data(self, token_data):
		raise NotImplementedError("Please Override this method in child classes")


class AccessTokenBearer(TokenBearer):
	def verify_token_data(self, token_data: dict) -> None:
		if token_data and token_data["refresh"]:
			raise AccessTokenRequired()


class RefreshTokenBearer(TokenBearer):
	def verify_token_data(self, token_data: dict) -> None:
		if token_data and not token_data["refresh"]:
			raise RefreshTokenRequired()

async def get_current_user(
		token_details: dict = Depends(AccessTokenBearer()),
		session: AsyncSession = Depends(get_session)
):
	user_username = token_details["user"]["username"]
	user = await user_service.get_user_by_username(user_username, session)
	return user


class RoleChecker:
	def __init__(self, allowed_roles: List[str]) -> None:
		self.allowed_roles = allowed_roles

	def __call__(self, current_user: User = Depends(get_current_user)) -> Any:
		if not current_user:
			raise UserNotFound()

		if current_user.role not in self.allowed_roles:
			raise InsufficientPermission()


async def get_user_or_404(
		user_id: str,
		session: AsyncSession = Depends(get_session)
) -> User:
	select_query = select(User).where(User.uid == user_id)
	result = await session.execute(select_query)
	user = result.scalar_one_or_none()
	return user






