import uvicorn
from fastapi import FastAPI

from app.routers import users

app = FastAPI(
	title="Тек Блок",
	description="Api for manage daily tasks",
	version="1.0.0",
	contacts="Diarra Moustapha",
)

app.include_router(users.router)

@app.get('/')
def root_controller():
	return {"status": "healthy"}

if __name__ == "__main__":
	uvicorn.run("main:app", port=8000, reload=True)