from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.main import get_session
from app.errors import VoltageNotFound
from app.voltage.schemas import Voltage, VoltageCreateModel
from app.voltage.service import VoltageService

voltage_router = APIRouter(tags=['Voltage'])
voltage_service = VoltageService()

@voltage_router.get("/", response_model=List[Voltage])
async def get_all_voltage(session: AsyncSession = Depends(get_session)):
	voltages = await voltage_service.get_all_voltages(session)

	return voltages


@voltage_router.get("/{voltage_id}", response_model=Voltage)
async def get_voltage(
		voltage_id: str,
		session: AsyncSession = Depends(get_session)
):
	voltage = await voltage_service.get_voltage(voltage_id, session)

	return voltage


@voltage_router.post("/", response_model=Voltage, status_code=status.HTTP_201_CREATED)
async def create_voltage(
		voltage_data: VoltageCreateModel,
		session: AsyncSession = Depends(get_session)
):
	new_voltage = await voltage_service.create_voltage(voltage_data, session)

	return new_voltage


@voltage_router.delete("/{voltage_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_voltage(
		voltage_id: str,
		session: AsyncSession = Depends(get_session)
):
	voltage_to_delete = await voltage_service.delete_voltage(voltage_id, session)

	if voltage_to_delete is None:
		return VoltageNotFound()
	else:
		return {}