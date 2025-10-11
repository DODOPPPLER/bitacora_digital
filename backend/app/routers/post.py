from fastapi import APIRouter, status, Depends
from backend.app.models.post import Post
from backend.app.utils.security import get_api_key
from backend.app.services.post_services import *

router = APIRouter(
    prefix="/post",
    tags=["post"],
    dependencies=[Depends(get_api_key)],
    responses={status.HTTP_404_NOT_FOUND: {"message": "No encontrado"}}
)

@router.get("/", response_model=list[Post])
async def posts():
    return get_posts
    
@router.get("/{id}", response_model=Post)
async def posts(id:str):
    return get_post("id_post",id)

@router.post("/", response_model=Post, status_code=status.HTTP_201_CREATED)
async def crear_post(post:Post):
    return  create_post(post)

@router.put("/", response_model=Post)
async def actualizar_post(post:Post):
    return update_post(post)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_post(id:int):
    return delete_post(id)