from backend.app.models.perfil import perfil

def perfiles_schema(perfiles):
    return[perfil(id_perfil=row[0], id_usuario=row[1], nombre=row[2], apellido=row[3], bio=row[4], foto_perfil=row[5]) for row in perfiles]

def perfil_schema(perfil_data):
    return perfil(id_perfil=perfil_data[0], id_usuario=perfil_data[1], nombre=perfil_data[2], apellido=perfil_data[3], bio=perfil_data[4], foto_perfil=perfil_data[5])