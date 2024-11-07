import re
from typing import Any, Self, Optional
from uuid import uuid4, UUID

from pydantic import BaseModel, Field, field_validator
from pydantic_core.core_schema import FieldValidationInfo


class User(BaseModel):
	full_name: str
	password: str

	@field_validator("password")
	def validate_password(cls, value: str, info: FieldValidationInfo) -> str:
		if len(value) < 8:
			raise ValueError("Password must be minimum 8 characters!")
		pattern = r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@!#$%^&*()_+=\-]).+$"
		if not re.match(pattern, value):
			raise ValueError(
				"Password must contains (@!#$%^&*()_+=-)."
			)
		return value


class CreateUserRequest(User):
	pass


class UpdateUserRequest(BaseModel):
	full_name: Optional[str] = None


class ChangePasswordRequest(BaseModel):
	old_password: str
	new_password: str
	confirm_password: str

class UserOut(BaseModel):
	user_id: UUID = Field(default_factory=uuid4)
	full_name: str

	class Config:
		from_attributes = True
