import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, HttpUrl


class TaskBase(BaseModel):
	code: str
	dispatcher_name: str
	location: str
	planner_date: str
	work_type: str
	voltage_class: float


class CreateTask(TaskBase):
	completion_date: Optional[datetime] = None
	latitude: Optional[float] = None
	longitude: Optional[float] = None
	photo_url_1: Optional[HttpUrl] = None
	photo_url_2: Optional[HttpUrl] = None
	comments: Optional[str] = None
	supervisor: Optional[str] = None


class TaskUpdate(BaseModel):
	completion_date: Optional[datetime] = None
	photo_url_1: Optional[HttpUrl] = None
	photo_url_2: Optional[HttpUrl] = None
	comments: Optional[str] = None


class TaskComplete(TaskBase):
	task_id: uuid.UUID
	completion_date: Optional[datetime] = None
	latitude: Optional[float] = None
	longitude: Optional[float] = None
	photo_url_1: Optional[HttpUrl] = None
	photo_url_2: Optional[HttpUrl] = None
	comments: Optional[str] = None
	supervisor: Optional[str] = None

	class Config:
		from_attributes = True
		arbitrary_types_allowed = True