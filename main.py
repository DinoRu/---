import uvicorn
from fastapi import FastAPI

from app.routers import users, tasks, healthcheck

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

app.include_router(healthcheck.router)
app.include_router(users.router)
app.include_router(tasks.router)

@app.get('/')
def root_controller():
	return {"status": "healthy"}

if __name__ == "__main__":
	uvicorn.run("main:app", port=8000, reload=True)