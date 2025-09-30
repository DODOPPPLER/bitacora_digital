from fastapi import APIRouter, HTTPException, status
from backend.app.models.usuario import Usuario
from backend.app.db.client import cur 

router = APIRouter(
    prefix="/usuario",
    tags=["usuario"],
    responses={status.HTTP_404_NOT_FOUND: {"message": "No encontrado"}}
)

def get_roles():
    cur.execute("SELECT * FROM rol")
    rows = cur.fetchall()
    # roles = [Rol(id=row[0], name=row[1], description=row[2]) for row in rows]
    return rows


@router.get("/", response_model=list[Usuario])
async def roles():
    return get_roles()
