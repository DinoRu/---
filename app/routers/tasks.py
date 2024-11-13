# from http.client import HTTPException
import io
import uuid
from typing import List

from fastapi import APIRouter, status, Depends, HTTPException, File, UploadFile
from openpyxl import load_workbook
from sqlalchemy.ext.asyncio import AsyncSession

from app.authentication import get_current_user
from app.controllers.tasks import task_controller
from app.database import get_session
from app.schemas.tasks import TaskComplete, CreateTask, TaskUpdate
from app.schemas.users import UserOut

router = APIRouter(
	prefix="/tasks",
	tags=["Tasks"],
	responses={404: {"description": "Not found."}}
)

@router.post("/upload",
			 status_code=status.HTTP_201_CREATED,
			 response_model=List[TaskComplete],
			 summary="Upload file (.xlsx)")
async def import_tasks_from_excel(
		file: UploadFile = File(...),
		session: AsyncSession = Depends(get_session)
):
	# if not file.filename.endswith(".xlsx"):
	# 	raise HTTPException(
	# 		status_code=status.HTTP_400_BAD_REQUEST,
	# 		detail="Only .xlsx files are supported."
	# 	)
	# Load the Excel file
	file.file.seek(0)
	content = file.file.read()
	workbook = load_workbook(io.BytesIO(content))
	sheet = workbook.active
	tasks = []
	for row in range(2, sheet.max_row + 1):
		try:
			task_data = CreateTask(
				task_id=uuid.uuid4(),
				code=str(sheet.cell(row=row, column=1).value)
							if sheet.cell(row=row, column=1).value else None,
				dispatcher_name=str(sheet.cell(row=row, column=2).value) if
							sheet.cell(row=row, column=2).value else None,
				location=str(sheet.cell(row=row, column=3).value) if sheet.cell(
					row=row, column=3
				).value else None,
				planner_date=str(sheet.cell(row=row, column=4).value)
							if sheet.cell(row=row, column=4).value else None,
				voltage_class=sheet.cell(row=row, column=5).value
								if sheet.cell(row=row, column=5).value else None,
				work_type=str(sheet.cell(row=row, column=6).value)
							if sheet.cell(row=row, column=6).value else None,
				completion_date=None,
				latitude=None,
				longitude=None,
				photo_url_1=None,
				photo_url_2=None,
				supervisor=None,
				comment=None
			)
		except KeyError as e:
			raise HTTPException(
				status_code=400, detail=f"Missing column in the Excel file: {e}"
			)
		task = await task_controller.add_task(session=session, data=task_data)
		tasks.append(task)
	total = len(tasks)
	print(total)
	return tasks


@router.put("/task/{task_id}",
			status_code=status.HTTP_200_OK,
			summary="Update task.",
			response_model=TaskComplete)
async def completed_task(
		task_id: uuid.UUID,
		data: TaskUpdate,
		session: AsyncSession = Depends(get_session),
		user: UserOut = Depends(get_current_user)
):
	return await task_controller.modify_task(
		session=session,
		task_id=task_id,
		update_data=data,
		username=user.username
	)

@router.get("/",
			status_code=status.HTTP_200_OK,
			summary="Get all tasks",
			response_model=List[TaskComplete]
			)
async def get_all_tasks(
		session: AsyncSession = Depends(get_session)
):
	return await task_controller.all(session=session)

@router.get("/task/{task_id}",
			status_code=status.HTTP_200_OK,
			summary="Get Task by task_ID.",
			response_model=TaskComplete)
async def get_one_or_404(
		task_id: uuid.UUID,
		session: AsyncSession = Depends(get_session)
):
	return await task_controller.get_task_or_404(session, task_id)

@router.delete("/",
			   status_code=status.HTTP_200_OK,
			   summary="Delete all Tasks.")
async def remove_all_tasks(
		session: AsyncSession = Depends(get_session)
):
	return await task_controller.delete_all(session=session)


@router.delete("/task/{task_id}", status_code=status.HTTP_200_OK,
			   summary="Remove task by Task_ID.")
async def remove_task(
		task_id: uuid.UUID,
		session: AsyncSession = Depends(get_session)
):
	return await task_controller.delete_or_404(session=session, task_id=task_id)