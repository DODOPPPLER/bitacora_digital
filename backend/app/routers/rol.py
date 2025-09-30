from fastapi import APIRouter, HTTPException, status
from backend.app.models.rol import Rol
from backend.app.schemas.rol import roles_schema, role_schema
from backend.app.db.client import cur 

router = APIRouter(
    prefix="/rol",
    tags=["rol"],
    responses={status.HTTP_404_NOT_FOUND: {"message": "No encontrado"}}
)

def get_roles():
    cur.execute("SELECT * FROM rol")
    roles = roles_schema(cur.fetchall())
    return roles

def get_rol(campo:str, registro:str):

    query = f"SELECT * FROM rol WHERE {campo}={registro}"
    cur.execute(query)
    row = cur.fetchone()
    if row:
        return role_schema(row)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Rol no encontrado")
    

@router.get("/", response_model=list[Rol])
async def roles():
    return get_roles()

@router.get("/{id}", response_model=Rol)
async def rol(id:str):
    return get_rol("id_rol", id)

@router.post("/", response_model=Rol, status_code=status.HTTP_201_CREATED)
async def crear_rol(rol:Rol):

    cur.execute("INSERT INTO rol (nombre, descripcion) VALUES (%s, %s) RETURNING *", (rol.nombre, rol.descripcion))
    nuevo_rol = cur.fetchone()
    if not nuevo_rol:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error al crear el rol")
    cur.connection.commit()

    return role_schema(nuevo_rol)

@router.put("/", response_model=Rol)
async def actualizar_rol(rol:Rol):

    get_rol("id_rol", rol.id_rol)
    cur.execute("UPDATE rol SET nombre=%s, descripcion=%s WHERE id_rol=%s RETURNING *", (rol.nombre, rol.descripcion, rol.id_rol))
    rol_actualizado = cur.fetchone()
    if not rol_actualizado:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error al actualizar el rol")
    cur.connection.commit()

    return role_schema(rol_actualizado)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_rol(id:int):
    get_rol("id_rol", id)
    cur.execute("DELETE FROM rol WHERE id_rol=%s RETURNING *", (id,))
    rol_eliminado = cur.fetchone()
    if not rol_eliminado:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error al eliminar el rol")
    
    cur.connection.commit()