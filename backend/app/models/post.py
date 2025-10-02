from pydantic import BaseModel
from datetime import datetime

class Post(BaseModel):
    id_post: int | None = None
    id_usuario: int
    titulo: str
    contenido: str
    fecha_creacion: datetime | None = None
    fecha_actualizacion: datetime | None = None
