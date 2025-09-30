import sys
sys.path.append('k:/PC/Proyectos/bitacora_digital')

from backend.app.models.rol import Rol

def roles_schema(roles):
    return[
        Rol(id_rol=row[0], nombre=row[1], descripcion=row[2]) for row in roles
    ]

def role_schema(role):
    return Rol(id_rol=role[0], nombre=role[1], descripcion=role[2])