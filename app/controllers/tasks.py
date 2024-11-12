import uuid
from datetime import datetime
from typing import Optional, List

import requests
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.tasks import task_repository
from app.schemas.tasks import CreateTask, TaskComplete, TaskUpdate
from app.schemas.users import UserOut
from app.utils.photo_metadata import photo_metadata


class TaskController:

	@classmethod
	async def add_task(cls, session: AsyncSession, data: CreateTask) -> TaskComplete:
		new_task = await task_repository.create_task(
			session=session,
			data=data
		)
		if not new_task:
			raise HTTPException(
				status_code=status.HTTP_400_BAD_REQUEST,
				detail="Invalid data provided."
			)
		return TaskComplete.from_orm(new_task)

	@classmethod
	async def modify_task(cls, session: AsyncSession,
						  task_id: uuid.UUID,
						  username: str,
						  update_data: TaskUpdate) -> Optional[TaskComplete]:
		completed_task = await task_repository.update(
			session=session,
			task_id=task_id,
			update_data=update_data,
			user_name=username
		)
		return completed_task

	@classmethod
	async def all(cls, session: AsyncSession) -> List[TaskComplete]:
		tasks = await task_repository.get_tasks(session=session)
		if not tasks:
			raise HTTPException(
				status_code=status.HTTP_404_NOT_FOUND,
				detail="Tasks not found."
			)
		return tasks

	@classmethod
	async def get_task_or_404(cls, session: AsyncSession, task_id: uuid.UUID) -> TaskComplete:
		task = await task_repository.get_task(session=session, task_id=task_id)
		if not task:
			raise HTTPException(
				status_code=status.HTTP_404_NOT_FOUND,
				detail="Task not found."
			)
		return task

	@classmethod
	async def delete_all(cls, session: AsyncSession):
		success = await task_repository.delete_tasks(session=session)
		if not success:
			raise HTTPException(
				status_code=status.HTTP_404_NOT_FOUND,
				detail="No Task found."
			)
		return {"detail": "Tasks deleted successfully."}

	@classmethod
	async def delete_or_404(cls, session: AsyncSession, task_id: uuid.UUID):
		success = await task_repository.delete_task(session=session, task_id=task_id)
		if not success:
			raise HTTPException(
				status_code=status.HTTP_404_NOT_FOUND,
				detail="Task not Found."
			)
		return {"detail": "Task deleted successfully."}

task_controller = TaskController()