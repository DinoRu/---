from enum import Enum


class TaskStatus(str, Enum):
    EXECUTING = "Выполняется"
    COMPLETED = "Выполнено"