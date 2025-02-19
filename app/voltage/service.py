
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select, desc, asc

from app.db.models import Voltage
from app.errors import VoltageNotFound
from app.voltage.schemas import VoltageCreateModel


class VoltageService:

	async def get_all_voltages(self, session: AsyncSession):
		stmt = select(Voltage).order_by(asc(Voltage.volt))

		result = await session.execute(stmt)
		return result.scalars().all()

	async def get_voltage(self, voltage_id: str, session: AsyncSession):
		stmt = select(Voltage).where(Voltage.uid == voltage_id)

		result = await session.execute(stmt)

		return result.scalar_one_or_none()

	async def create_voltage(self, voltage_data: VoltageCreateModel, session: AsyncSession):
		voltage_data_dict =voltage_data.model_dump()

		voltage = Voltage(**voltage_data_dict)

		session.add(voltage)
		await session.commit()

		return voltage

	async def delete_voltage(self, voltage_id: str, session: AsyncSession):
		voltage_to_delete = await self.get_voltage(voltage_id, session)

		if voltage_to_delete is not None:
			await session.delete(voltage_to_delete)
			await session.commit()
			return {}
		else:
			return None
