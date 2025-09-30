from pydantic import BaseModel

class Rol(BaseModel):
    id_rol: int | None = None
    nombre: str
    descripcion: str | None = None