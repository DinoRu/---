import uuid
from datetime import datetime

from pydantic import BaseModel, Field


class UserCreateModel(BaseModel):
	username: str = Field(max_length=25)
	full_name: str = Field(max_length=30)
	role: str = Field(max_length=5)
	password: str = Field(min_length=6)

	model_config = {
		"json_schema_extra": {
			"example": {
				"username": "kamil",
				"full_name": "Kamil Ramazanov",
				"role": "user",
				"password": "testpass123!"
			}
		}
	}

class UserModel(BaseModel):
	uid: uuid.UUID
	username: str
	full_name: str
	role: str
	password_hash: str = Field(exclude=True)
	created_at: datetime
	updated_at: datetime


class UserLoginModel(BaseModel):
	username: str = Field(max_length=25)
	password: str = Field(min_length=6)

