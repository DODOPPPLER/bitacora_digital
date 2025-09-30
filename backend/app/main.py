from fastapi import FastAPI
from backend.app.routers import rol, usuario

app = FastAPI()

app.include_router(rol.router)
app.include_router(usuario.router)
