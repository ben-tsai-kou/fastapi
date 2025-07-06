from fastapi import FastAPI
import models
from database import engine
from auth import router as auth_router
from todo import router as todo_router

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(auth_router.router)
app.include_router(todo_router.router)
