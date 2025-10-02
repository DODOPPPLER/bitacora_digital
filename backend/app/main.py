from fastapi import FastAPI
from backend.app.routers import rol, usuario, post, perfil

app = FastAPI()

app.include_router(rol.router)
app.include_router(usuario.router)
app.include_router(post.router)
app.include_router(perfil.router)

