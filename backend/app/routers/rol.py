from fastapi import APIRouter, status, Depends
from backend.app.models.rol import Rol
from backend.app.utils.security import get_api_key
from backend.app.services.rol_services import *

router = APIRouter(
    prefix="/rol",
    tags=["rol"],
    dependencies=[Depends(get_api_key)],
    responses={status.HTTP_404_NOT_FOUND: {"message": "No encontrado"}}
) 

@router.get("/", response_model=list[Rol])
async def roles():
    return get_roles()

@router.get("/{id}", response_model=Rol)
async def rol(id:str):
    return get_rol("id_rol", id)

@router.post("/", response_model=Rol, status_code=status.HTTP_201_CREATED)
async def crear_rol(rol:Rol):
    return create_rol(rol)

@router.put("/", response_model=Rol)
async def actualizar_rol(rol:Rol):

    return update_rol(rol)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_rol(id:int):
    
    return delete_rol(id)