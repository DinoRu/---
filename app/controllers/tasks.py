import uuid
from datetime import datetime
from typing import Optional, List

import requests
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.tasks import task_repository
from app.schemas.tasks import CreateTask, TaskComplete, TaskUpdate, AddNewTask
from app.schemas.users import UserOut
from app.utils.excel import get_file_from_database
from app.utils.photo_metadata import photo_metadata
from app.utils.status import TaskStatus


class TaskController:

	@classmethod
	async def add_new_task(cls, session: AsyncSession, data: AddNewTask, supervisor: str):
		new_task = await task_repository.add_new_task(
			session=session,
			data=data,
			username=supervisor
		)
		if not new_task:
			raise HTTPException(
				status_code=status.HTTP_400_BAD_REQUEST,
				detail="Invalid data provided."
			)
		return TaskComplete.from_orm(new_task)

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
	async def get_by_status(cls, session: AsyncSession, task_status: TaskStatus) -> List[TaskComplete]:
		tasks = await task_repository.get_task_by_status(status=task_status, session=session)
		if not tasks:
			raise HTTPException(
				status_code=status.HTTP_404_NOT_FOUND,
				detail="Tasks not found."
			)
		return tasks

	@classmethod
	async def get_completed_tasks(cls, session: AsyncSession) -> List[TaskComplete]:
		completed_tasks = await task_repository.get_completed_task(session)
		if not completed_tasks:
			raise HTTPException(
				status_code=status.HTTP_404_NOT_FOUND,
				detail="Tasks not available."
			)
		return completed_tasks

	@classmethod
	async def get_pending_tasks(cls, session: AsyncSession) -> List[TaskComplete]:
		pending_tasks= await task_repository.get_pending_task(session)
		if not pending_tasks:
			raise HTTPException(
				status_code=status.HTTP_404_NOT_FOUND,
				detail="Tasks not found."
			)
		return pending_tasks

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

	@classmethod
	async def get_completed_tasks_by_supervisor(cls, session: AsyncSession, username: str) -> List[TaskComplete]:
		tasks = await task_repository.get_completed_tasks_by_username(session, username)
		return tasks

	@classmethod
	async def get_completed_tasks_files(cls, session: AsyncSession):
		tasks = await task_repository.get_completed_task(session)
		file = get_file_from_database(tasks)
		return file

	@classmethod
	async def get_tasks_by_user(cls, session: AsyncSession, location: str = None) -> List[TaskComplete]:
		tasks = await task_repository.get_task_by_user(session=session, location=location)
		return tasks

	@classmethod
	async def get_tasks_completed_by_user(cls, session: AsyncSession, location: str = None) -> List[TaskComplete]:
		tasks = await task_repository.get_task_completed_by_user(session, location)
		return tasks


task_controller = TaskController()