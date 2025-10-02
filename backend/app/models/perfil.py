from pydantic import BaseModel 

class perfil(BaseModel):
    id_perfil: int | None = None
    id_usuario: int
    nombre: str
    apellido: str | None = None
    bio: str | None = None
    foto_perfil: str | None = None