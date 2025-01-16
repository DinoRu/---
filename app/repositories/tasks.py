import uuid
from datetime import datetime
from typing import Optional, List

import requests
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.tasks import Task
from app.schemas.tasks import CreateTask, TaskUpdate, AddNewTask
from app.utils.photo_metadata import photo_metadata
from app.utils.status import TaskStatus


class TaskRepository:

	@classmethod
	async def add_new_task(cls, session: AsyncSession, data: AddNewTask, username: str) -> Task:
		photo = requests.get(data.photo_url_1)
		if photo.status_code != 200:
			raise ValueError(
				f"Photo not downloaded."
			)
		coordinates = photo_metadata.get_coordinate(photo.content)
		if coordinates:
			latitude = coordinates.latitude
			longitude = coordinates.longitude
		else:
			latitude = 0.0
			longitude = 0.0
		supervisor = username
		completion_date = datetime.now().strftime("%d-%m-%Y %H:%M")
		new_task = Task(
			task_id=data.task_id,
			code=data.code,
			dispatcher_name=data.dispatcher_name,
			location=data.location,
			planner_date=data.planner_date,
			work_type=data.work_type,
			voltage_class=data.voltage_class,
			completion_date=completion_date,
			latitude=latitude,
			longitude=longitude,
			photo_url_1=data.photo_url_1,
			photo_url_2=data.photo_url_2,
			supervisor=supervisor,
			comments=data.comments,
			status=data.status
		)
		session.add(new_task)
		await session.commit()
		await session.refresh(new_task)
		return new_task

	@classmethod
	async def create_task(cls, session: AsyncSession,  data: CreateTask) -> Task:
		task = Task(
			task_id=data.task_id,
			code=data.code,
			dispatcher_name=data.dispatcher_name,
			location=data.location,
			planner_date=data.planner_date,
			work_type=data.work_type,
			voltage_class=data.voltage_class,
			completion_date=data.completion_date,
			latitude=data.latitude,
			longitude=data.longitude,
			photo_url_1=data.photo_url_1,
			photo_url_2=data.photo_url_2,
			supervisor=data.supervisor,
			comments=data.comments
		)
		session.add(task)
		await session.commit()
		await session.refresh(task)
		return task

	@classmethod
	async def get_tasks(cls, session: AsyncSession):
		stmt = select(Task)
		result = await session.execute(stmt)
		return result.scalars().all()

	@classmethod
	async def get_task(cls, session: AsyncSession, task_id: uuid.UUID):
		stmt = select(Task).where(Task.task_id == task_id)
		result = await session.execute(stmt)
		return result.scalar_one_or_none()

	@classmethod
	async def get_pending_task(cls, session: AsyncSession):
		stmt = select(Task).where(Task.status == TaskStatus.EXECUTING)
		result = await session.execute(stmt)
		return result.scalars().all()

	@classmethod
	async def get_task_by_status(cls, session: AsyncSession, status: TaskStatus):
		stmt = select(Task).where(Task.status == status)
		result = await session.execute(stmt)
		return result.scalars().all()

	@classmethod
	async def update(cls, session: AsyncSession, task_id: uuid.UUID,
					 update_data: TaskUpdate, user_name: str) -> Optional[Task]:
		task = await cls.get_task(session, task_id)
		if not task:
			return None
		for key, value in update_data.dict(exclude_unset=True).items():
			setattr(task, key, value)
		photo = requests.get(task.photo_url_1)
		if photo.status_code != 200:
			raise ValueError(
				f"Photo not downloaded."
			)
		coordinates = photo_metadata.get_coordinate(photo.content)
		if not coordinates:
			raise ValueError(
				f"Coordinates not found."
			)
		task.latitude = coordinates.latitude
		task.longitude = coordinates.longitude
		task.supervisor = user_name
		task.completion_date = datetime.now().strftime("%d-%m-%Y %H:%M")
		task.status = TaskStatus.COMPLETED
		await session.commit()
		await session.refresh(task)
		return task

	@classmethod
	async def delete_task(cls, session: AsyncSession, task_id: uuid.UUID) -> bool | None:
		stmt = delete(Task).where(Task.task_id == task_id)
		result = await session.execute(stmt)
		await session.commit()
		return result.rowcount > 0

	@classmethod
	async def delete_tasks(cls, session: AsyncSession) -> bool:
		stmt = delete(Task)
		result = await session.execute(stmt)
		await session.commit()
		return result.rowcount > 0


	@classmethod
	async def get_completed_task(cls, session: AsyncSession):
		stmt = select(Task).where(Task.status == TaskStatus.COMPLETED)
		result = await session.execute(stmt)
		return result.scalars().all()

	@classmethod
	async def get_completed_tasks_by_username(cls, session: AsyncSession, username: str):
		stmt = select(Task).where(Task.supervisor == username)
		result = await session.execute(stmt)
		return result.scalars().all()

	@classmethod
	async def get_task_by_user(cls, session: AsyncSession, location: str = None):
		query = select(Task)
		if location:
			stmt = query.where(
				Task.location.like(f"%{location}%"),
				Task.status == TaskStatus.EXECUTING.value
			)
			result = await session.execute(stmt)
		else:
			stmt = select(Task).where(
				Task.status == TaskStatus.EXECUTING.value
			)
			result = await session.execute(stmt)
		return result.scalars().all()

	@classmethod
	async def get_task_completed_by_user(cls, session: AsyncSession, location: str = None):
		query = select(Task)
		if location:
			stmt = query.where(
				Task.location.like(f"%{location}%"),
				Task.status == TaskStatus.COMPLETED.value
			)
			result = await session.execute(stmt)
		else:
			stmt = select(Task).where(
				Task.status == TaskStatus.COMPLETED.value
			)
			result = await session.execute(stmt)
		return result.scalars().all()

task_repository = TaskRepository()
