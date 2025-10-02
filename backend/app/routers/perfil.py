from fastapi import APIRouter, HTTPException, status
from backend.app.models.perfil import perfil
from backend.app.schemas.perfil import perfiles_schema, perfil_schema
from backend.app.db.client import cur

router = APIRouter(
    prefix="/perfil",
    tags=["perfil"],
    responses={status.HTTP_404_NOT_FOUND: {"message": "No encontrado"}}
)

def get_perfiles():
    cur.execute("SELECT * FROM perfil")
    perfiles = perfiles_schema(cur.fetchall())
    return perfiles

def get_perfil(campo: str, registro: str):
    # Lista de campos válidos para prevenir inyección SQL
    campos_validos = ["id_perfil", "id_usuario", "nombre"]
    if campo not in campos_validos:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Campo no válido")
    
    query = f"SELECT * FROM perfil WHERE {campo}=%s"
    cur.execute(query, (registro,))
    row = cur.fetchone()
    if row:
        return perfil_schema(row)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Perfil no encontrado")

@router.get("/", response_model=list[perfil])
async def perfiles():
    return get_perfiles()

@router.get("/{id}", response_model=perfil)
async def perfil_by_id(id: str):
    return get_perfil("id_perfil", id)

@router.get("/usuario/{id_usuario}", response_model=perfil)
async def perfil_by_usuario(id_usuario: str):
    return get_perfil("id_usuario", id_usuario)

@router.post("/", response_model=perfil, status_code=status.HTTP_201_CREATED)
async def crear_perfil(nuevo_perfil: perfil):
    cur.execute("INSERT INTO perfil (id_usuario, nombre, apellido, bio, foto_perfil) VALUES (%s, %s, %s, %s, %s) RETURNING *", 
                (nuevo_perfil.id_usuario, nuevo_perfil.nombre, nuevo_perfil.apellido, nuevo_perfil.bio, nuevo_perfil.foto_perfil))
    perfil_creado = cur.fetchone()
    
    # Confirmar la transacción
    cur.connection.commit()
    
    if not perfil_creado:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error al crear el perfil")
    
    return perfil_schema(perfil_creado)

@router.put("/", response_model=perfil)
async def actualizar_perfil(perfil_actualizado: perfil):
    cur.execute("UPDATE perfil SET id_usuario=%s, nombre=%s, apellido=%s, bio=%s, foto_perfil=%s WHERE id_perfil=%s RETURNING *", 
                (perfil_actualizado.id_usuario, perfil_actualizado.nombre, perfil_actualizado.apellido, 
                 perfil_actualizado.bio, perfil_actualizado.foto_perfil, perfil_actualizado.id_perfil))
    perfil_updated = cur.fetchone()
    
    if not perfil_updated:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error al actualizar el perfil")
    
    cur.connection.commit()
    return perfil_schema(perfil_updated)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_perfil(id: int):
    cur.execute("DELETE FROM perfil WHERE id_perfil=%s RETURNING *", (id,))
    perfil_eliminado = cur.fetchone()
    
    if not perfil_eliminado:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Perfil no encontrado")
    
    cur.connection.commit()