import uuid
from datetime import datetime

from pydantic import BaseModel


class WorkType(BaseModel):
	uid: uuid.UUID
	title: str
	created_at: datetime


class WorkTypeCreateModel(BaseModel):
	title: str


class UpdateWorkType(BaseModel):
	title: str

