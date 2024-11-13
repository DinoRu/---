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


class CreateTask(BaseModel):
	task_id: uuid.UUID
	completion_date: Optional[datetime | None]
	latitude: float | None
	longitude: float | None
	photo_url_1: Optional[HttpUrl | None]
	photo_url_2: Optional[HttpUrl | None]
	comments: str | None
	supervisor: Optional[str | None]
	code: str
	dispatcher_name: str
	location: str
	planner_date: str
	work_type: str
	voltage_class: float


class TaskUpdate(BaseModel):
	photo_url_1: HttpUrl
	photo_url_2: HttpUrl
	comments: str | None


class TaskComplete(BaseModel):
	task_id: uuid.UUID
	completion_date: datetime | None
	latitude: float | None
	longitude: float | None
	photo_url_1: HttpUrl | None
	photo_url_2: HttpUrl | None
	comments: str | None
	supervisor: str | None
	code: str
	dispatcher_name: str
	location: str
	planner_date: str
	work_type: str
	voltage_class: float

	class Config:
		from_attributes = True