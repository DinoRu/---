from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class TaskBase(BaseModel):
	dispatcher_name: str
	address: str
	planner_date: Optional[str] = None
	work_type: str
	voltage: float
	job: Optional[str] = None
	photo_url_1: Optional[str] = None
	photo_url_2: Optional[str] = None
	photo_url_3: Optional[str] = None
	photo_url_4: Optional[str] = None
	photo_url_5: Optional[str] = None
	comments: Optional[str] = None


class TaskRead(TaskBase):
	id: int
	supervisor: Optional[str] = None
	completion_date: Optional[str] = None
	created_at: datetime


class TaskCreate(TaskBase):
	pass


class TaskUpdate(BaseModel):
	photo_url_1: Optional[str] = None
	photo_url_2: Optional[str] = None
	photo_url_3: Optional[str] = None
	photo_url_4: Optional[str] = None
	photo_url_5: Optional[str] = None
	comments: Optional[str] = None
