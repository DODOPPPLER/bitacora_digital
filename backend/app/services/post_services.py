from backend.app.models.post import Post
from backend.app.schemas.post import post_schema, posts_schema
from backend.app.db.client import cur
from fastapi import HTTPException, status

def get_posts():
    cur.execute("SELECT * FROM posts")
    posts = cur.fetchall()
    return posts_schema(posts)

def get_post(campo:str, registro:str):
    query = f"SELECT * FROM post WHERE {campo}=%s"
    cur.execute(query,(registro))
    post = cur.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post no encontrado")
    return post_schema(post)

def create_post(post:Post):
    try:
        get_post("contenido", post.contenido)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Este post ya existe")
    except HTTPException as e:
        if e.status_code != status.HTTP_404_NOT_FOUND:
            raise e
        
    cur.execute("INSERT INTO post (id_usuario, titulo, contenido) VALUES (%s, %s, %s) RETURNING *", (post.id_usuario, post.titulo, post.contenido))
    nuevo_post = cur.fetchone()
    if not nuevo_post:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error al crear el post")
    cur.connection.commit()

def update_post(post:Post):
    try:
        get_post("contenido", post.contenido)
        post.fecha_actualizacion = None

        cur.execute("UPDATE post SET id_usuario=%s, titulo=%s, contenido=%s, fecha_actualizacion=%s WHERE id_post=%s RETURNING *", (post.id_usuario, post.titulo, post.contenido, post.fecha_actualizacion, post.id_post))
        post_actualizado=cur.fetchone()
        if not post_actualizado:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error al actualizar el post")
        cur.connection.commit()

        return post_schema(post_actualizado)
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El post no existe")

def delete_post(id:int):
    cur.execute("DELETE FROM post WHERE id_post=%s RETURNING *", (id,))
    post_eliminado = cur.fetchone()
    if not post_eliminado:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error al eliminar el post")
    cur.connection.commit()

    return post_eliminado

    
