import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.auth.routes import auth_router
from app.routers import users, tasks, healthcheck
from app.tasks.routes import task_router
from app.voltage.routes import voltage_router
from app.workType.routes import work_type_router

app = FastAPI(
	title="Тек Блок",
	description="API для управления ежедневными задачами",
	version="1.0.0",
	contacts="Diarra Moustapha",
	openapi_url="/api/v1/openapi.json",
	swagger_ui_parameters={
        "persistAuthorization": True
    },
)

#Register the origins
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


app.include_router(healthcheck.router)
app.include_router(auth_router, prefix="/auth", tags=['User'])
app.include_router(task_router, prefix="/task", tags=["Tasks"])
app.include_router(work_type_router, prefix="/workType")
app.include_router(voltage_router, prefix="/voltage")


@app.get('/')
def root_controller():
	return {"status": "healthy"}

if __name__ == "__main__":
	uvicorn.run("main:app", port=8000, reload=True)