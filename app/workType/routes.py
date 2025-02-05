from typing import List

from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.main import get_session
from app.errors import WorkTypeNotFound
from app.workType.schemas import WorkType, WorkTypeCreateModel
from app.workType.service import WorkTypeService

work_type_router = APIRouter(tags=['workType'])

work_type_service = WorkTypeService()

@work_type_router.get("/",
					  status_code=status.HTTP_200_OK,
					  response_model=List[WorkType])
async def get_all_work_type(
		session: AsyncSession = Depends(get_session)
):
	work_types = await work_type_service.get_all_work_type(session)

	return work_types


@work_type_router.get("/{work_type_id}", response_model=WorkType)
async def get_work_type(
		work_type_id: str,
		session: AsyncSession = Depends(get_session)
):
	work_type = await work_type_service.get_work_by_uid(work_type_id, session)

	return work_type


@work_type_router.post("/", status_code=status.HTTP_201_CREATED, response_model=WorkType)
async def create_work_type(
		work_type_data: WorkTypeCreateModel,
		session: AsyncSession = Depends(get_session)
):
	new_work_type = await work_type_service.create_work_type(session, work_type_data)

	return new_work_type


@work_type_router.delete("/{work_type_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_work_type(
		work_type_id: str,
		session: AsyncSession = Depends(get_session)
):
	work_type_delete = await work_type_service.delete_work_type(work_type_id, session)

	if work_type_delete is None:
		return WorkTypeNotFound()
	else:
		return {}
