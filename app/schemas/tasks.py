import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.utils.status import TaskStatus


class TaskBase(BaseModel):
	code: str
	dispatcher_name: str
	location: str
	planner_date: str
	work_type: str
	voltage_class: float


class CreateTask(BaseModel):
	task_id: uuid.UUID
	code: str
	dispatcher_name: str
	location: str
	planner_date: str
	work_type: str
	completion_date: Optional[str | None]
	voltage_class: float
	latitude: float | None
	longitude: float | None
	photo_url_1: Optional[str | None]
	photo_url_2: Optional[str | None]
	comments: str | None
	supervisor: Optional[str | None]
	status: TaskStatus


class TaskUpdate(BaseModel):
	photo_url_1: str
	photo_url_2: str
	comments: str | None


class TaskComplete(BaseModel):
	task_id: uuid.UUID
	code: str
	dispatcher_name: str
	location: str
	planner_date: str
	work_type: str
	completion_date: str | None
	voltage_class: float
	latitude: float | None
	longitude: float | None
	photo_url_1: str | None
	photo_url_2: str | None
	comments: str | None
	supervisor: str | None
	status: TaskStatus

	class Config:
		from_attributes = True