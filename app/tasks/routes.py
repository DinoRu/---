import io
from typing import List

from fastapi import APIRouter, Depends, status, File, UploadFile, HTTPException
from openpyxl.reader.excel import load_workbook
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import AccessTokenBearer, RoleChecker
from app.db.main import get_session
from app.db.models import Task
from app.errors import TaskNotFound, InsufficientPermission
from app.tasks.schemas import TaskRead, TaskCreate, TaskUpdate
from app.tasks.service import TaskService

task_router = APIRouter()
task_service = TaskService()
access_token_bearer = AccessTokenBearer()
role_checker = Depends(RoleChecker(['admin', 'user']))

@task_router.get("/", response_model=List[Task], dependencies=[role_checker])
async def get_all_tasks(
		session: AsyncSession = Depends(get_session),
		_: dict = Depends(access_token_bearer)
):
	tasks = await task_service.get_all_tasks(session)
	return tasks

@task_router.get("/{task_id}", response_model=TaskRead, dependencies=[role_checker])
async def get_task(
		task_id: int,
		session: AsyncSession = Depends(get_session),
		_: dict = Depends(access_token_bearer)
) -> dict:
	task = await task_service.get_task(task_id, session)

	if task:
		return task
	else:
		raise TaskNotFound


@task_router.post(
	"/",
	status_code=status.HTTP_201_CREATED,
	response_model=TaskRead,
	dependencies=[role_checker]
)
async def create_a_task(
		task_data: TaskCreate,
		session: AsyncSession = Depends(get_session),
		token_details: dict = Depends(access_token_bearer)
):
	username = token_details.get("user")["username"]
	new_task = await task_service.create_a_task(task_data, username, session)
	return new_task


@task_router.post(
	"/upload",
	status_code=status.HTTP_201_CREATED,
	response_model=List[TaskRead]
)
async def upload_file(
		uploadFile: UploadFile = File(...),
		session: AsyncSession = Depends(get_session),
):
	uploadFile.file.seek(0)
	content = uploadFile.file.read()
	workbook = load_workbook(io.BytesIO(content))
	sheet = workbook.active
	tasks = []
	for row in range(3, sheet.max_row + 1):
		try:
			new_task = TaskCreate(
				work_type=str(sheet.cell(row=row, column=2).value) if sheet.cell(row=row, column=2).value else None,
				dispatcher_name=str(sheet.cell(row=row, column=3).value) if sheet.cell(row=row, column=3).value else None,
				address=str(sheet.cell(row=row, column=4).value) if sheet.cell(row=row, column=4).value else None,
				planner_date=str(sheet.cell(row=row, column=5).value) if sheet.cell(row=row, column=5).value else None,
				voltage=sheet.cell(row=row, column=7).value if sheet.cell(row=row, column=7).value else None,
				job=str(sheet.cell(row=row, column=8).value) if sheet.cell(row=row, column=8).value else None,
				photo_url_1=None,
				photo_url_2=None,
				photo_url_3=None,
				photo_url_4=None,
				photo_url_5=None,
				comments=None
			)
		except KeyError as e:
			raise HTTPException(
				status_code=400, detail=f"Missing column in the Excel file: {e}"
			)
		task = await task_service.create_tasks(new_task, session)
		tasks.append(task)
	return tasks


@task_router.patch(
	"/{task_id}",
	response_model=TaskRead,
	dependencies=[role_checker]
)
async def update_task(
		task_id: int, task_update_data: TaskUpdate, session: AsyncSession = Depends(get_session),
		token_details: dict = Depends(access_token_bearer)
):
	username = token_details.get('user')["username"]
	updated_task = await task_service.update_task(task_id, task_update_data, session, username)
	if updated_task is None:
		raise TaskNotFound
	else:
		return updated_task


@task_router.delete(
	"/{task_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[role_checker]
)
async def delete_task(
		task_id: int, session: AsyncSession = Depends(get_session),
		token_data: dict = Depends(access_token_bearer)
):
	role = token_data.get('user')['role']
	if role == 'admin':
		task_to_delete = await task_service.task_delete(task_id, session)

		if task_to_delete is None:
			raise TaskNotFound
		else:
			return {}
	else:
		raise InsufficientPermission()


@task_router.delete(
	"/clear", status_code=status.HTTP_204_NO_CONTENT, dependencies=[role_checker]
)
async def delete_all_tasks(
		session: AsyncSession = Depends(get_session)
):
	all_tasks = await task_service.tasks_delete(session)
	return all_tasks
