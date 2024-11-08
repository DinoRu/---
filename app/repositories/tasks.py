import uuid
from datetime import datetime
from typing import Optional

import requests
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.tasks import Task
from app.schemas.tasks import CreateTask, TaskUpdate
from app.utils.photo_metadata import photo_metadata


class TaskRepository:

	@classmethod
	async def create_task(cls, session: AsyncSession,  data: CreateTask) -> Task:
		task = Task(**data.dict())
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
		coordinates = photo_metadata.get_coordinate(photo)
		if not coordinates:
			raise ValueError(
				f"Coordinates not found."
			)
		task.latitude = coordinates.latitude
		task.longitude = coordinates.longitude
		task.supervisor = user_name
		task.completion_date = datetime.now().strftime("%d-%m-%Y")
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


task_repository = TaskRepository()
