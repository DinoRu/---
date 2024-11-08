import uuid
from datetime import datetime
from typing import Optional

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
						  user: UserOut,
						  update_data: TaskUpdate) -> Optional[TaskComplete]:
		task = await task_repository.get_task(session=session, task_id=task_id)
		if not task:
			raise HTTPException(
				status_code=status.HTTP_404_NOT_FOUND,
				detail='Task not found.'
			)
		return TaskComplete.from_orm(task)


