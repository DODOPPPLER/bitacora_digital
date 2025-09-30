from fastapi import APIRouter, HTTPException, status
from backend.app.models.usuario import Usuario, UsuarioCreate, UsuarioResponse
from backend.app.schemas.usuario import usuarios_schema, usuario_schema, usuario_schema_update
from backend.app.db.client import cur 

router = APIRouter(
    prefix="/usuario",
    tags=["usuario"],
    responses={status.HTTP_404_NOT_FOUND: {"message": "No encontrado"}}
)

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

@router.get("/", response_model=list[UsuarioResponse])
async def usuarios():
    return get_usuarios()

@router.get("/{id}", response_model=UsuarioResponse)
async def usuarios(id:str):
    return get_usuario("id_usuario",id)


@router.post("/", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
async def crear_usuario(usuario:UsuarioCreate):

    cur.execute("INSERT INTO usuario (nombre_usuario, email, contraseña, id_rol) VALUES (%s, %s, %s, %s) RETURNING id_usuario, nombre_usuario, email, id_rol", (usuario.nombre_usuario, usuario.email, usuario.contraseña, usuario.id_rol))
    nuevo_usuario = cur.fetchone()

    if not nuevo_usuario:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error al crear el usuario")
    cur.connection.commit()

    return  usuario_schema(nuevo_usuario)

@router.put("/", response_model=Usuario)
async def actualizar_usuario(usuario:Usuario):
    
    cur.execute("UPDATE usuario SET nombre_usuario=%s, email=%s, contraseña=%s, id_rol=%s WHERE id_usuario=%s RETURNING *", (usuario.nombre_usuario, usuario.email, usuario.contraseña, usuario.id_rol, usuario.id_usuario))
    usuario_actualizado = cur.fetchone()
    if not usuario_actualizado:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error al actualizar el usuario")
    cur.connection.commit()

    return usuario_schema_update(usuario_actualizado)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_usuario(id:int):
    cur.execute("DELETE FROM usuario WHERE id_usuario=%s RETURNING *", (id,))
    usuario_eliminado = cur.fetchone()
    if not usuario_eliminado:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error al eliminar el usuario")
    cur.connection.commit()

    return usuario_eliminado

