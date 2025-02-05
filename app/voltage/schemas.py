import uuid
from datetime import datetime

from pydantic import BaseModel


class Voltage(BaseModel):
	uid: uuid.UUID
	volt: float
	created_at: datetime


class VoltageCreateModel(BaseModel):
	volt: float


