from backend.app.models.usuario import Usuario, UsuarioCreate, UsuarioResponse

def usuarios_schema(usuarios):
    return[UsuarioResponse(id_usuario=row[0], nombre_usuario=row[1], email=row[2], id_rol=row[3]) for row in usuarios]

def usuario_schema(usuario):
    return UsuarioResponse(id_usuario=usuario[0], nombre_usuario=usuario[1], email=usuario[2], id_rol=usuario[3])

def usuario_schema_update(usuario):
    return Usuario(id_usuario=usuario[0], nombre_usuario=usuario[1], email=usuario[2], contraseña=usuario[3], id_rol=usuario[4])