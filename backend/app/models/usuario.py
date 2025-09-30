from pydantic import BaseModel

class Usuario(BaseModel):
    id_usuario: int | None = None
    nombre_usuario: str
    email: str
    contraseña: str
    id_rol: int

class UsuarioCreate(BaseModel):
    nombre_usuario: str
    email: str
    contraseña: str
    id_rol: int

class UsuarioResponse(BaseModel):
    id_usuario: int
    nombre_usuario: str
    email: str
    id_rol: int
    