import uuid

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy_utils import UUIDType

from app.database import Base


class User(Base):
	__tablename__ = "users"

	user_id: Mapped[uuid.UUID] = mapped_column(
								primary_key=True, index=True, default=uuid.uuid4)
	username: Mapped[str] = mapped_column(unique=True, index=True)
	full_name: Mapped[str]
	location: Mapped[str] = mapped_column(nullable=True)
	password: Mapped[str]


	def __str__(self):
		return f"User {self.full_name}"