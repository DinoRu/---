import uuid
from typing import Optional

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.tasks import Task
from app.schemas.tasks import CreateTask, TaskUpdateRequest, TaskComplete


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
					 data: TaskUpdateRequest, user_name: str) -> Optional[TaskComplete]:
		task = await cls.get_task(session, task_id)
		if not task:
			return None
		for key, value in data.dict(exclude_unset=True).items():
			setattr(task, key, value)
		task.supervisor = user_name
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
