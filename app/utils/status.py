from enum import Enum


class TaskStatus(str, Enum):
    EXECUTING = "Выполняется"
    COMPLETED = "Выполнено"


class UserRole(str, Enum):
    ADMIN = "admin"
    USER = "user"
    GUEST = "guest"
    WORKER = "worker"