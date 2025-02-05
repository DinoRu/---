from typing import Callable, Any
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from fastapi import FastAPI, status
from sqlalchemy.exc import SQLAlchemyError


class TaskException(Exception):
    """This is the base class for all task-related errors."""
    pass


class InvalidToken(TaskException): pass
class RevokedToken(TaskException): pass
class AccessTokenRequired(TaskException): pass
class RefreshTokenRequired(TaskException): pass
class UserAlreadyExists(TaskException): pass
class InvalidCredentials(TaskException): pass
class InsufficientPermission(TaskException): pass
class TaskNotFound(TaskException): pass
class UserNotFound(TaskException): pass
class WorkTypeNotFound(TaskException): pass
class VoltageNotFound(TaskException): pass


def create_exception_handler(
    status_code: int, initial_detail: Any
) -> Callable[[Request, Exception], JSONResponse]:

    async def exception_handler(request: Request, exc: TaskException):
        return JSONResponse(
            content={"message": str(exc), "error_code": initial_detail["error_code"]},
            status_code=status_code,
        )

    return exception_handler


def register_all_errors(app: FastAPI):
    exceptions = {
        UserAlreadyExists: (403, "User already exists", "user_exists"),
        UserNotFound: (404, "User not found", "user_not_found"),
        TaskNotFound: (404, "Task not found", "task_not_found"),
        WorkTypeNotFound: (404, "Work type not found", "work_type_not_found"),
        VoltageNotFound: (404, "Voltage type not found", "voltage_type_not_found"),
        InvalidCredentials: (400, "Invalid username or password", "invalid_credentials"),
        InvalidToken: (401, "Invalid or expired token", "invalid_token"),
        RevokedToken: (401, "Token revoked", "token_revoked"),
        AccessTokenRequired: (401, "Access token required", "access_token_required"),
        RefreshTokenRequired: (403, "Refresh token required", "refresh_token_required"),
        InsufficientPermission: (401, "Insufficient permissions", "insufficient_permissions"),
    }

    for exc_class, (status_code, message, error_code) in exceptions.items():
        app.add_exception_handler(
            exc_class,
            create_exception_handler(
                status_code=status_code,
                initial_detail={"message": message, "error_code": error_code},
            ),
        )

    @app.exception_handler(SQLAlchemyError)
    async def database_error(request, exc):
        return JSONResponse(
            content={
                "message": "Database error occurred",
                "details": str(exc),
                "error_code": "database_error",
            },
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
