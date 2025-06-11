import uuid

from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlmodel import select

from app.db.main import get_session
from app.db.models import Task


async def get_task_or_404(
		task_id: int,
		session: AsyncSession = Depends(get_session)
):
	stmt = select(Task).where(Task.id == task_id)
	result = await session.execute(stmt)
	task = result.scalar_one_or_none()
	if not task:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task does not found")
	return task