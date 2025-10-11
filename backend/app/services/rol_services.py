from backend.app.models.rol import Rol
from backend.app.schemas.rol import roles_schema, role_schema
from backend.app.db.client import cur
from fastapi import HTTPException, status

def get_roles():
    cur.execute("SELECT * FROM rol")
    roles = cur.fetchall()
    return roles_schema(roles)


def get_rol(campo:str, registro:str):
    query = f"SELECT * FROM rol WHERE {campo}=%s"
    cur.execute(query, (registro,))
    rol = cur.fetchone()
    if not rol:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Rol no encontrado")
    return role_schema(rol)

def create_rol(rol:Rol):
    try:
        get_rol("nombre", rol.nombre)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El rol ya existe")
    except HTTPException as e:
        if e.status_code != status.HTTP_404_NOT_FOUND:
            raise e
        
    cur.execute("INSERT INTO rol (nombre, descripcion) VALUES (%s, %s) RETURNING *", (rol.nombre, rol.descripcion))
    nuevo_rol = cur.fetchone()
    if not nuevo_rol:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error al crear el rol")
    
    cur.connection.commit()
    return role_schema(nuevo_rol)

def update_rol(rol:Rol):
    try:
        get_rol("id_rol", rol.id_rol)
        
        cur.execute("UPDATE rol SET nombre=%s, descripcion=%s WHERE id_rol=%s RETURNING *", (rol.nombre, rol.descripcion, rol.id_rol))
        rol_actualizado = cur.fetchone()
        if not rol_actualizado:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error al actualizar el rol")
        cur.connection.commit()
        return rol_actualizado
        
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El rol no existe")


def delete_rol(id):
    try:
        get_rol("id_rol", id)
        cur.execute("DELETE FROM rol WHERE id_rol=%s RETURNING *", (id,))
        rol_eliminado = cur.fetchone()
        if not rol_eliminado:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error al eliminar el rol")
        cur.connection.commit()

    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error al eliminar el rol si no existe")
    
