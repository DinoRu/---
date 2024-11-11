from fastapi import HTTPException, status
from jose import jwt
from jose.exceptions import JWEError

from app.config import settings


def create_access_token(user: dict):
	payload = {
		"user": user
	}
	token = jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)
	return token


def verify_access_token(token: str):
	try:
		data = jwt.decode(token, settings.secret_key, algorithms=settings.algorithm)
		return data
	except JWEError:
		raise HTTPException(
			status_code=status.HTTP_400_BAD_REQUEST,
			detail="Invalid token."
		)