from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.repositories.users import user_repository
from app.utils.jwt_handler import verify_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")

async def get_current_user(
		token: str = Depends(oauth2_scheme),
		session: AsyncSession = Depends(get_session)
):
	credential_exception = HTTPException(
		status_code=status.HTTP_401_UNAUTHORIZED,
		detail="Could not validate credentials.",
		headers={"WWW-Authenticate": "Bearer"}
	)
	if not token:
		raise HTTPException(
			status_code=status.HTTP_403_FORBIDDEN,
			detail="Sign in to access."
		)
	data = verify_access_token(token=token)
	payload = data.get("user", {})
	user_id = payload.get("user_id")
	if not user_id:
		raise credential_exception
	user = await user_repository.get_user(session, user_id)
	if not user:
		raise credential_exception
	return user