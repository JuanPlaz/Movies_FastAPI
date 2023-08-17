from fastapi import APIRouter
from utils.jwt_manager import create_token
from fastapi.responses import JSONResponse
from schemas.user import User

user_router = APIRouter()


@user_router.post('/login', tags=['auth'])  #Se crea path en donde se ejecutará el login/token
def login(user: User):
    if user.email == "admin@gmail.com" and user.password == "admin":    #Habiendo definido las credenciales
        token:str = create_token(user.dict()) #Se llama a la funcion "create_token" y el servidor nos contesta con el token
        return JSONResponse(status_code=200, content=token)