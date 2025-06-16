from datetime import datetime
from typing import Optional, List
from uuid import UUID

from pydantic import BaseModel, conlist, Field

from app.auth.schemas import UserModel


class TaskBase(BaseModel):
	dispatcher_name: str
	address: str
	planner_date: Optional[str] = None
	job: Optional[str] = None
	photos: Optional[List[str]] = Field(default=None, max_length=5)
	comments: Optional[str] = None


class TaskRead(TaskBase):
	id: int
	work_type: Optional[str]
	voltage: Optional[float]
	latitude: Optional[float] = None
	longitude: Optional[float] = None
	completion_date: Optional[str] = None
	created_at: datetime
	is_completed: bool

	worker: Optional[UserModel] = None


class TaskCreate(TaskBase):
	work_type: str
	voltage: float



class TaskUpdate(BaseModel):
	photos: Optional[List[str]] = Field(default=None, min_length=2, max_length=5)
	comments: Optional[str] = None
