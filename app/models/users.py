import uuid

from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class User(Base):
	__tablename__ = "users"

	user_id: Mapped[uuid.UUID] = mapped_column(primary_key=True, index=True, default=uuid.uuid4())
	full_name: Mapped[str]
	password: Mapped[str]


	def __str__(self):
		return f"User {self.full_name}"