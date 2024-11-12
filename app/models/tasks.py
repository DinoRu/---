import uuid
from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Task(Base):
	__tablename__ = "tasks"

	task_id: Mapped[uuid.UUID] = mapped_column(primary_key=True, index=True, default=uuid.uuid4())
	code: Mapped[str]
	dispatcher_name: Mapped[str]
	location: Mapped[str]
	planner_date: Mapped[str]
	work_type: Mapped[str]
	completion_date: Mapped[datetime] = mapped_column(default=None, nullable=True)
	voltage_class: Mapped[float]
	latitude: Mapped[float | None] = mapped_column(nullable=True)
	longitude: Mapped[float | None] = mapped_column(nullable=True)
	photo_url_1: Mapped[str | None]
	photo_url_2: Mapped[str | None]
	comments: Mapped[str | None]
	supervisor: Mapped[str | None]

	def __str__(self):
		return f'Task {self.task_id}'
