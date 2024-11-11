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
	if not file.filename.endswith(".xlsx"):
		raise HTTPException(
			status_code=status.HTTP_400_BAD_REQUEST,
			detail="Only .xlsx files are supported."
		)
	# Load the Excel file
	upload_file = file.file.read()
	try:
		workbook = load_workbook(io.BytesIO(upload_file))
		sheet = workbook.active
	except Exception as e:
		raise HTTPException(
			status_code=status.HTTP_400_BAD_REQUEST,
			detail="Invalid Excel file."
		)
	tasks = []
	for row in sheet.iter_rows(min_row=2, values_only=True):  # Skip header
		# Parse each row and map it to a CreateTask schema, handling empty cells as None
		try:
			task_data = CreateTask(
				code=row[0],
				dispatcher_name=row[1] if row[1] is not None else None,
				location=row[2] if row[2] is not None else None,
				planned_date=row[3] if row[3] is not None else None,
				voltage_class=row[4] if row[4] is not None else None,
				work_type=row[5] if row[5] is not None else None,
				completion_date=None,
				latitude=None,
				longitude=None,
				photo_url_1=None,
				photo_url_2=None,
				supervisor=None,
				comment=None
			)
			new_task = await task_controller.add_task(session=session, data=task_data)
			tasks.append(new_task)
		except Exception as e:
			raise HTTPException(
				status_code=status.HTTP_400_BAD_REQUEST,
				detail=f"Error processing row {row}: {str(e)}"
			) from e
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
