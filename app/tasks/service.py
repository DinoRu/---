from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select, desc, delete

from app.db.models import Task
from app.tasks.schemas import TaskCreate, TaskUpdate
from app.tasks.utils import get_file_from_database
from app.utils.get_lat_long import get_coordinates_from_photo
from app.utils.photo_metadata import photo_metadata


class TaskService:

	async def get_all_tasks(self, session: AsyncSession):
		statement = select(Task).where(Task.is_completed == False).order_by(desc(Task.created_at))

		result = await session.execute(statement)

		return result.scalars().all()

	async def get_task(self, task_id: int, session: AsyncSession):
		statement = select(Task).where(Task.id == task_id)
		result = await session.execute(statement)

		return result.scalar_one_or_none()

	async def create_task_from_file(self, task_data: TaskCreate, session: AsyncSession):

		task_data_dict = task_data.model_dump(exclude_unset=True)
		new_task = Task(**task_data_dict)

		session.add(new_task)

		await session.commit()

		await session.refresh(new_task)

		return new_task

	async def create_a_task(self, task_data: TaskCreate, username: str, session: AsyncSession):
		coordinates = None
		# Utiliser les deux premières photos pour obtenir les coordonnées
		if task_data.photos and len(task_data.photos) >= 2:
			coordinates = photo_metadata.get_coordinate_from_url(task_data.photos[0])
			if not coordinates:
				coordinates = photo_metadata.get_coordinate_from_url(task_data.photos[1])

		task_data_dict = task_data.model_dump()
		new_task = Task(
			**task_data_dict,
			completion_date=datetime.now().strftime("%d-%m-%Y %H:%M"),
			is_completed=True
		)

		if coordinates:
			new_task.longitude = coordinates.longitude
			new_task.latitude = coordinates.latitude

		session.add(new_task)
		await session.commit()
		await session.refresh(new_task)
		return new_task


	async def update_task(
			self, task_id: int,
			update_data: TaskUpdate,
			session: AsyncSession,
			username: str
	):
		task_to_update = await self.get_task(task_id, session)
		if not task_to_update:
			return None

		update_data_dict = update_data.model_dump(exclude_unset=True)

		# Gestion des coordonnées à partir des photos
		coordinates = None
		if 'photos' in update_data_dict and update_data_dict['photos']:
			photos = update_data_dict['photos']
			if len(photos) > 0:
				coordinates = photo_metadata.get_coordinate_from_url(photos[0])
			if not coordinates and len(photos) > 1:
				coordinates = photo_metadata.get_coordinate_from_url(photos[1])

			if coordinates:
				update_data_dict['latitude'] = coordinates.latitude
				update_data_dict['longitude'] = coordinates.longitude

		# Mise à jour des champs
		for key, value in update_data_dict.items():
			setattr(task_to_update, key, value)

		task_to_update.supervisor = username
		task_to_update.completion_date = datetime.now().strftime("%d-%m-%Y %H:%M")
		task_to_update.is_completed = True

		await session.commit()
		await session.refresh(task_to_update)
		return task_to_update


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
		stmt = select(Task).where(Task.is_completed == True).order_by(desc(Task.created_at))
		result = await session.execute(stmt)
		tasks = result.scalars().all()
		return tasks
