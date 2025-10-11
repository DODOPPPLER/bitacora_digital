from backend.app.models.usuario import Usuario, UsuarioCreate, UsuarioResponse
from backend.app.schemas.usuario import usuario_schema, usuario_schema_update, usuarios_schema
from backend.app.db.client import cur
from fastapi import HTTPException, status

def get_usuarios():
    cur.execute("SELECT id_usuario, nombre_usuario, email, id_rol FROM usuario")
    usuarios = usuarios_schema(cur.fetchall())
    return usuarios

def get_usuario(campo:str, registro:str):
    query = f"SELECT id_usuario, nombre_usuario, email, id_rol FROM usuario WHERE {campo}={registro}"
    cur.execute(query)
    row = cur.fetchone()

    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
    
    return usuario_schema(row)

def create_usuario(usuario:UsuarioCreate):
    try:
        get_usuario("id_usuario",id)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
    except HTTPException as e:
        if e.status_code != status.HTTP_404_NOT_FOUND:
            raise e
    
    cur.execute("INSERT INTO usuario (nombre_usuario, email, contraseña, id_rol) VALUES (%s, %s, %s, %s) RETURNING id_usuario, nombre_usuario, email, id_rol", (usuario.nombre_usuario, usuario.email, usuario.contraseña, usuario.id_rol))
    nuevo_usuario = cur.fetchone()

    if not nuevo_usuario:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error al crear el usuario")
    cur.connection.commit()

    return  usuario_schema(nuevo_usuario)
    
def update_usuario(usuario:Usuario):

    try:
        get_usuario("id_usuario",id)

        cur.execute("UPDATE usuario SET nombre_usuario=%s, email=%s, contraseña=%s, id_rol=%s WHERE id_usuario=%s RETURNING *", (usuario.nombre_usuario, usuario.email, usuario.contraseña, usuario.id_rol, usuario.id_usuario))
        usuario_actualizado = cur.fetchone()
        if not usuario_actualizado:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error al actualizar el usuario")
        cur.connection.commit()

        return usuario_actualizado

    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El usuario no existe")
    
def delete_usuario():

    try:
        get_usuario("id_usuario",id)

        cur.execute("DELETE FROM usuario WHERE id_usuario=%s RETURNING *", (id,))
        usuario_eliminado = cur.fetchone()
        if not usuario_eliminado:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error al eliminar el usuario")
        cur.connection.commit()
        return usuario_eliminado
    
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El usuario no existe")