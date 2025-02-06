from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select, desc, delete

from app.db.models import Task
from app.schemas.tasks import TaskUpdate
from app.tasks.schemas import TaskCreate
from app.tasks.utils import get_file_from_database


class TaskService:

	async def get_all_tasks(self, session: AsyncSession):
		statement = select(Task).order_by(desc(Task.created_at))

		result = await session.execute(statement)

		return result.scalars().all()

	async def get_task(self, task_id: int, session: AsyncSession):
		statement = select(Task).where(Task.id == task_id)
		result = await session.execute(statement)

		return result.scalar_one_or_none()

	async def create_tasks(self, task_data: TaskCreate, session: AsyncSession):
		task_data_dict = task_data.model_dump(exclude_unset=True)
		new_task = Task(**task_data_dict)

		session.add(new_task)

		await session.commit()

		return new_task

	async def create_a_task(self, task_data: TaskCreate, username: str, session: AsyncSession):
		task_data_dict = task_data.model_dump()
		new_task = Task(**task_data_dict)

		new_task.supervisor = username
		new_task.completion_date = datetime.now().strftime("%d-%m-%Y %H:%M")
		new_task.is_completed = True

		session.add(new_task)
		await session.commit()
		await session.refresh(new_task)

		return new_task

	async def update_task(
			self, task_id: int, update_data: TaskUpdate, session: AsyncSession,
			username: str
	):
		task_to_update = await self.get_task(task_id, session)

		if task_to_update is not None:
			update_data_dict = update_data.model_dump(exclude_unset=True)

			for k, v in update_data_dict.items():
				setattr(task_to_update, k, v)

			task_to_update.supervisor = username
			task_to_update.completion_date = datetime.now().strftime("%d-%m-%Y %H:%M")
			task_to_update.is_completed = True

			await session.commit()
			await session.refresh(task_to_update)

			return task_to_update
		else:
			return None

	async def task_delete(self, task_id: int, session: AsyncSession):
		task_to_delete = await self.get_task(task_id, session)

		if task_to_delete is not None:
			await session.delete(task_to_delete)

			await session.commit()

			return {}
		else:
			return None

	async def tasks_delete(self, session: AsyncSession):
		statement = delete(Task)
		await session.execute(statement)
		await session.commit()
		return  {}

	async def get_tasks_completed(self, session: AsyncSession):
		stmt = select(Task).where(Task.is_completed == True)
		result = await session.execute(stmt)
		tasks = result.scalars().all()
		return tasks
