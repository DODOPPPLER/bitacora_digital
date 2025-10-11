from backend.app.models.perfil import perfil
from backend.app.schemas.perfil import perfiles_schema, perfil_schema
from backend.app.db.client import cur
from fastapi import HTTPException, status

def get_perfiles():
    cur.execute("SELECT * FROM perfil")
    perfiles = cur.fetchall()
    return perfiles_schema(perfiles)

def get_perfil(campo: str, registro: str):
    # Lista de campos válidos para prevenir inyección SQL
    campos_validos = ["id_perfil", "id_usuario", "nombre"]
    if campo not in campos_validos:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Campo no válido")
    
    query = f"SELECT * FROM perfil WHERE {campo}=%s"
    cur.execute(query, (registro,))
    row = cur.fetchone()
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Perfil no encontrado")
    return perfil_schema(row)

def create_perfil(nuevo_perfil: perfil):
    # Verificar si el usuario ya tiene un perfil
    try:
        get_perfil("id_usuario", str(nuevo_perfil.id_usuario))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El usuario ya tiene un perfil")
    except HTTPException as e:
        if e.status_code != status.HTTP_404_NOT_FOUND:
            raise e
    
    # Verificar que el usuario existe
    cur.execute("SELECT COUNT(*) FROM usuario WHERE id_usuario=%s", (nuevo_perfil.id_usuario,))
    if cur.fetchone()[0] == 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El usuario no existe")
    
    # Crear el perfil
    cur.execute("INSERT INTO perfil (id_usuario, nombre, apellido, bio, foto_perfil) VALUES (%s, %s, %s, %s, %s) RETURNING *", 
                (nuevo_perfil.id_usuario, nuevo_perfil.nombre, nuevo_perfil.apellido, nuevo_perfil.bio, nuevo_perfil.foto_perfil))
    perfil_creado = cur.fetchone()
    
    if not perfil_creado:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error al crear el perfil")
    
    cur.connection.commit()
    return perfil_schema(perfil_creado)

def update_perfil(perfil_actualizado: perfil):
    try:
        # Verificar que el perfil existe
        get_perfil("id_perfil", str(perfil_actualizado.id_perfil))
        
        # Verificar que el usuario existe
        cur.execute("SELECT COUNT(*) FROM usuario WHERE id_usuario=%s", (perfil_actualizado.id_usuario,))
        if cur.fetchone()[0] == 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El usuario no existe")
        
        # Verificar si está cambiando de usuario y que ese usuario no tenga ya un perfil
        cur.execute("SELECT id_usuario FROM perfil WHERE id_perfil=%s", (perfil_actualizado.id_perfil,))
        usuario_actual = cur.fetchone()[0]
        
        if usuario_actual != perfil_actualizado.id_usuario:
            try:
                get_perfil("id_usuario", str(perfil_actualizado.id_usuario))
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El nuevo usuario ya tiene un perfil")
            except HTTPException as e:
                if e.status_code != status.HTTP_404_NOT_FOUND:
                    raise e
        
        # Actualizar el perfil
        cur.execute("UPDATE perfil SET id_usuario=%s, nombre=%s, apellido=%s, bio=%s, foto_perfil=%s WHERE id_perfil=%s RETURNING *", 
                    (perfil_actualizado.id_usuario, perfil_actualizado.nombre, perfil_actualizado.apellido, 
                     perfil_actualizado.bio, perfil_actualizado.foto_perfil, perfil_actualizado.id_perfil))
        perfil_updated = cur.fetchone()
        
        if not perfil_updated:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error al actualizar el perfil")
        
        cur.connection.commit()
        return perfil_schema(perfil_updated)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error al actualizar el perfil")

def delete_perfil(id_perfil):
    try:
        # Verificar que el perfil existe
        get_perfil("id_perfil", str(id_perfil))
        
        # Eliminar el perfil
        cur.execute("DELETE FROM perfil WHERE id_perfil=%s RETURNING *", (id_perfil,))
        perfil_eliminado = cur.fetchone()
        
        if not perfil_eliminado:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error al eliminar el perfil")
        
        cur.connection.commit()
        return perfil_eliminado
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error al eliminar el perfil")

def get_perfil_by_usuario(id_usuario: str):
    """Función específica para obtener perfil por usuario"""
    return get_perfil("id_usuario", id_usuario)
