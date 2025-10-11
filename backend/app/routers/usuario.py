from fastapi import APIRouter, status, Depends
from backend.app.models.usuario import Usuario, UsuarioCreate, UsuarioResponse
from backend.app.schemas.usuario import usuarios_schema, usuario_schema, usuario_schema_update
from backend.app.utils.security import get_api_key
from backend.app.services.usuario_services import *

router = APIRouter(
    prefix="/usuario",
    tags=["usuario"],
    dependencies=[Depends(get_api_key)],
    responses={status.HTTP_404_NOT_FOUND: {"message": "No encontrado"}}
)

@router.get("/", response_model=list[UsuarioResponse])
async def usuarios():
    return get_usuarios()

@router.get("/{id}", response_model=UsuarioResponse)
async def usuarios(id:str):
    return get_usuario("id_usuario",id)


@router.post("/", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
async def crear_usuario(usuario:UsuarioCreate):
    return create_usuario(usuario)

@router.put("/", response_model=Usuario)
async def actualizar_usuario(usuario:Usuario):
    return update_usuario

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_usuario(id:int):
    return delete_usuario(id)   

