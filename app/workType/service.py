from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select, desc

from app.db.models import WorkType
from app.workType.schemas import WorkTypeCreateModel


class WorkTypeService:

	async def create_work_type(self, session: AsyncSession, work_type_data: WorkTypeCreateModel):
		work_type_data_dict = work_type_data.model_dump()
		new_work_type = WorkType(**work_type_data_dict)

		session.add(new_work_type)

		await session.commit()
		await session.refresh(new_work_type)
		return  new_work_type

	async def get_work_by_uid(self, work_type_uid: str, session: AsyncSession):
		statement = select(WorkType).where(WorkType.uid == work_type_uid)
		result = await session.execute(statement)

		work_type = result.scalar_one_or_none()
		return work_type

	async def get_all_work_type(self, session):
		statement = select(WorkType)

		result = await session.execute(statement)
		work_types = result.scalars().all()
		return work_types

	async def delete_work_type(self, work_type_uid: str, session: AsyncSession):
		work_type = await self.get_work_by_uid(work_type_uid, session)

		if work_type is not None:
			await session.delete(work_type)
			await session.commit()
			return {}
		else:
			return None
