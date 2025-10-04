from fastapi import APIRouter, HTTPException, status, Depends
from backend.app.models.post import Post
from backend.app.schemas.post import posts_schema, post_schema
from backend.app.db.client import cur 
from backend.app.utils.security import get_api_key


router = APIRouter(
    prefix="/post",
    tags=["post"],
    dependencies=[Depends(get_api_key)],
    responses={status.HTTP_404_NOT_FOUND: {"message": "No encontrado"}}
)

def get_posts():
    cur.execute("SELECT * FROM post")
    posts = posts_schema(cur.fetchall())
    return posts

def get_post(campo:str, registro:str):
    query = f"SELECT * FROM post WHERE {campo}={registro}"  
    cur.execute(query)
    post = post_schema(cur.fetchone())

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post no encontrado")
    
    return post

@router.get("/", response_model=list[Post])
async def posts():
    return get_posts()

@router.get("/{id}", response_model=Post)
async def posts(id:str):
    return get_post("id_post",id)

@router.post("/", response_model=Post, status_code=status.HTTP_201_CREATED)
async def crear_post(post:Post):

    post.fecha_creacion = None

    cur.execute("INSERT INTO post (id_usuario, titulo, contenido) VALUES (%s, %s, %s) RETURNING *", (post.id_usuario, post.titulo, post.contenido))
    nuevo_post = cur.fetchone()
    if not nuevo_post:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error al crear el post")
    cur.connection.commit()

    return  post_schema(nuevo_post)

@router.put("/", response_model=Post)
async def actualizar_post(post:Post):
    post.fecha_actualizacion = None

    cur.execute("UPDATE post SET id_usuario=%s, titulo=%s, contenido=%s, fecha_actualizacion=%s WHERE id_post=%s RETURNING *", (post.id_usuario, post.titulo, post.contenido, post.fecha_actualizacion, post.id_post))
    post_actualizado = cur.fetchone()
    if not post_actualizado:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error al actualizar el post")
    cur.connection.commit()

    return post_schema(post_actualizado)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_post(id:int):
    cur.execute("DELETE FROM post WHERE id_post=%s RETURNING *", (id,))
    post_eliminado = cur.fetchone()
    if not post_eliminado:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error al eliminar el post")
    cur.connection.commit()

    return post_eliminado