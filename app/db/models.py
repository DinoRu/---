import uuid
from datetime import datetime
from typing import Optional

import sqlalchemy.dialects.postgresql as pg
from sqlmodel import SQLModel, Field, Column


class User(SQLModel, table=True):
	__tablename__ = "users"
	uid: uuid.UUID = Field(sa_column=Column(pg.UUID, primary_key=True, default=uuid.uuid4))
	username: str = Field(sa_column=Column(pg.VARCHAR, unique=True, nullable=False))
	full_name: str
	role: str = Field(sa_column=Column(pg.VARCHAR, nullable=False, server_default='user'))
	password_hash: str = Field(sa_column=Column(pg.VARCHAR, nullable=False), exclude=True)
	created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, nullable=False, default=datetime.now))
	updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, nullable=False, onupdate=datetime.now, default=datetime.now))

	def __repr__(self):
		return f"<User {self.username}>"


class Task(SQLModel, table=True):
	__tablename__ = "tasks"
	id: int = Field(sa_column=Column(pg.INTEGER, primary_key=True, autoincrement=True))
	work_type: str = Field(foreign_key='work_types.title')
	dispatcher_name: str
	address: str
	planner_date: str = Field(sa_column=Column(pg.VARCHAR, nullable=True))
	voltage: float = Field(foreign_key="voltages.volt")
	job: Optional[str] = Field(sa_column=Column(pg.VARCHAR, nullable=True))
	latitude: float | None = Field(sa_column=Column(pg.FLOAT, nullable=True))
	longitude: float | None = Field(sa_column=Column(pg.FLOAT, nullable=True))
	photo_url_1: Optional[str] = Field(sa_column=Column(pg.VARCHAR, nullable=True))
	photo_url_2: Optional[str] = Field(sa_column=Column(pg.VARCHAR, nullable=True))
	photo_url_3: Optional[str] = Field(sa_column=Column(pg.VARCHAR, nullable=True))
	photo_url_4: Optional[str] = Field(sa_column=Column(pg.VARCHAR, nullable=True))
	photo_url_5: Optional[str] = Field(sa_column=Column(pg.VARCHAR, nullable=True))
	comments: Optional[str] = Field(sa_column=Column(pg.TEXT, nullable=True))
	supervisor: Optional[str] = Field(sa_column=Column(pg.VARCHAR, nullable=True))
	completion_date: str = Field(sa_column=Column(pg.VARCHAR, nullable=True))
	is_completed: bool = Field(sa_column=Column(pg.BOOLEAN, default=False))
	created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now, nullable=False))

	def __repr__(self):
		return f"<Task {self.uid}>"


class WorkType(SQLModel, table=True):
	__tablename__ = 'work_types'
	uid: uuid.UUID = Field(sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4))
	title: str = Field(sa_column=Column(pg.VARCHAR, unique=True, nullable=False))
	created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now, nullable=False))

	def __repr__(self):
		return f"<Work Type {self.title}>"


class Voltage(SQLModel, table=True):
	__tablename__ = "voltages"
	uid: uuid.UUID = Field(sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4))
	volt: float = Field(sa_column=Column(pg.FLOAT, unique=True, nullable=False))
	created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now, nullable=False))

	def __repr__(self):
		return f"<Voltage class {self.volt}>"
