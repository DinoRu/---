import logging
import uuid
from datetime import timedelta, datetime
from typing import Any

import jwt
from passlib.context import CryptContext

from app.settings import Config

passwd_context = CryptContext(schemes=["bcrypt"])
ACCESS_TOKEN_EXPIRY = 3600

def generate_passwd_hash(password: str) -> str:
	pwd_hash = passwd_context.hash(password)

	return pwd_hash

def verify_password(password: str, pwd_hash: str) -> bool:
	return passwd_context.verify(password, pwd_hash)


def create_access_token(
		user_data: dict,
		refresh: bool = False
):
	payload = {}

	payload["user"] = user_data
	payload["jti"] = str(uuid.uuid4())
	payload["refresh"] = refresh
	token = jwt.encode(
		payload=payload, key=Config.secret_key, algorithm=Config.algorithm
	)
	return token

def decode_token(token: str) -> Any | None:
	try:
		token_data = jwt.decode(
			jwt=token, key=Config.secret_key, algorithms=[Config.algorithm]
		)
		return token_data
	except jwt.PyJWTError as e:
		logging.exception(e)
		return None



