import uuid
from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Task(Base):
	__tablename__ = "tasks"

	task_id: Mapped[uuid.UUID] = mapped_column(primary_key=True, index=True, default=uuid.uuid4())
	code: Mapped[str]
	obj_name: Mapped[str]
	address: Mapped[str]
	according_date: Mapped[datetime]
	king_of_work: Mapped[str]
	completion_date: Mapped[datetime] = mapped_column(default=None, nullable=True)
	voltage: Mapped[float]
	latitude: Mapped[float | None] = mapped_column(nullable=True)
	longitude: Mapped[float | None] = mapped_column(nullable=True)
	photo_url_1: Mapped[str | None]
	photo_url_2: Mapped[str | None]
	comments: Mapped[str | None]
	supervisor: Mapped[str | None]

	def __str__(self):
		return f'Task {self.task_id}'
