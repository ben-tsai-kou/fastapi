from fastapi import FastAPI
from src.auth import models as auth_models

from src.todo import models as todo_models
from database import engine
from src.auth import router as auth_router
from src.todo import router as todo_router
from src.admin import router as admin_router
from src.users import router as users_router

app = FastAPI()

auth_models.Base.metadata.create_all(bind=engine)
todo_models.Base.metadata.create_all(bind=engine)


@app.get("/healthy")
def health_check():
    return {"status": "Healthy"}


app.include_router(auth_router.router)
app.include_router(todo_router.router)
app.include_router(admin_router.router)
app.include_router(users_router.router)
