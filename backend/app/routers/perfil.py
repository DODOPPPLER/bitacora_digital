from fastapi import APIRouter, status, Depends
from backend.app.models.perfil import perfil
from backend.app.utils.security import get_api_key
from backend.app.services.perfil_services import *

router = APIRouter(
    prefix="/perfil",
    tags=["perfil"],
    dependencies=[Depends(get_api_key)],
    responses={status.HTTP_404_NOT_FOUND: {"message": "No encontrado"}}
)

@router.get("/", response_model=list[perfil])
async def perfiles():
    return get_perfiles()

@router.get("/{id}", response_model=perfil)
async def perfil_by_id(id: str):
    return get_perfil("id_perfil", id)

@router.get("/usuario/{id_usuario}", response_model=perfil)
async def perfil_by_usuario(id_usuario: str):
    return get_perfil_by_usuario(id_usuario)

@router.post("/", response_model=perfil, status_code=status.HTTP_201_CREATED)
async def crear_perfil(nuevo_perfil: perfil):
    return create_perfil(nuevo_perfil)

@router.put("/", response_model=perfil)
async def actualizar_perfil(perfil_actualizado: perfil):
    return update_perfil(perfil_actualizado)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_perfil(id: int):
    return delete_perfil(id)