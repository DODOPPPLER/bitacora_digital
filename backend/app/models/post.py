from pydantic import BaseModel
from datetime import datetime

class post(BaseModel):
    id_post: int
    id_usuario: int
    titulo: str
    contenido: str
    fecha_creacion: datetime
    fecha_actualizacion: str | None = None