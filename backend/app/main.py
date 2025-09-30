from fastapi import FastAPI
from backend.app.routers import rol

app = FastAPI()

app.include_router(rol.router)
