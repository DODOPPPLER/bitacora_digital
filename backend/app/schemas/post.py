from backend.app.models.post import Post

def posts_schema(posts):
    return[Post(id_post=row[0], id_usuario=row[1], titulo=row[2], contenido=row[3], fecha_creacion=row[4], fecha_actualizacion=row[5]) for row in posts]

def post_schema(post):
    return Post(id_post=post[0], id_usuario=post[1], titulo=post[2], contenido=post[3], fecha_creacion=post[4], fecha_actualizacion=post[5])
