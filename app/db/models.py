import uuid
from datetime import datetime
from enum import Enum
from typing import Optional, List

import sqlalchemy.dialects.postgresql as pg
from sqlalchemy import CheckConstraint
from sqlalchemy.dialects.postgresql import ARRAY
from sqlmodel import SQLModel, Field, Column, Relationship

from app.utils.status import UserRole


class User(SQLModel, table=True):
    __tablename__ = "users"
    uid: uuid.UUID = Field(sa_column=Column(pg.UUID, primary_key=True, default=uuid.uuid4))
    username: str = Field(sa_column=Column(pg.VARCHAR, unique=True, nullable=False))
    full_name: str
    role: UserRole = Field(default=UserRole.USER, sa_column=Column(pg.VARCHAR, nullable=False))
    password_hash: str = Field(sa_column=Column(pg.VARCHAR, nullable=False), exclude=True)
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, nullable=False, default=datetime.now))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, nullable=False, onupdate=datetime.now, default=datetime.now))

    tasks: List["Task"] = Relationship(back_populates="worker")

    def __repr__(self):
        return f"<User {self.username}>"


class Task(SQLModel, table=True):
    __tablename__ = "tasks"
    __table_args__ = (
        CheckConstraint(
            "array_length(photos, 1) BETWEEN 2 AND 5",
            name='photos_length_check'
        ),
    )

    id: int = Field(sa_column=Column(pg.INTEGER, primary_key=True, autoincrement=True))
    dispatcher_name: str
    address: str
    planner_date: str = Field(sa_column=Column(pg.VARCHAR, nullable=True))
    work_type: str = Field(sa_column=Column(pg.VARCHAR, nullable=False))
    voltage: float = Field(sa_column=Column(pg.FLOAT, nullable=False))
    job: Optional[str] = Field(sa_column=Column(pg.VARCHAR, nullable=True))
    latitude: float | None = Field(sa_column=Column(pg.FLOAT, nullable=True))
    longitude: float | None = Field(sa_column=Column(pg.FLOAT, nullable=True))
    photos: Optional[List[str]] = Field(
        sa_column=Column(pg.ARRAY(pg.VARCHAR),
                         nullable=True,
                         ))
    comments: Optional[str] = Field(sa_column=Column(pg.TEXT, nullable=True))

    completion_date: str = Field(sa_column=Column(pg.VARCHAR, nullable=True))
    is_completed: bool = Field(sa_column=Column(pg.BOOLEAN, default=False))
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now, nullable=False))

    worker_id: Optional[uuid.UUID] = Field(default=None, foreign_key="users.uid", nullable=True, index=True )
    worker: Optional["User"] = Relationship(back_populates="tasks")


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
