from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel

from starlette.requests import Request
from jwt_manager import create_token
from config.database import engine, Base 

from middlewares.error_handler import Error_Handler
from routers.movie import movie_router

app = FastAPI()
app.title = "Mi aplicacion con FastAPI"
app.version = "0.0.3"

app.add_middleware(Error_Handler)   #Se linkea el error handler creado anteriormente.
app.include_router(movie_router)    #Se linkea el router con los metodos relacionados con Movies.

Base.metadata.create_all(bind= engine)

class User(BaseModel):
    email: str
    password: str


movies = [
    {
        "id": 1,
        "title": "Avatar",
        "overview": "En el gran planeta Pandora existe un valioso recurso...",
        "year": "2009",
        "rating": 7.8,
        "category": "Acción"
    },
    {
        "id": 2,
        "title": "Avatar 2",
        "overview": "En el gran planeta Pandora existe un valioso recurso...",
        "year": "2022",
        "rating": 9.1,
        "category": "Acción"
    }
]

@app.get('/', tags= ['Home'])
def message():
    return HTMLResponse('<h1>Hello World</h1>')

@app.post('/login', tags=['auth'])  #Se crea path en donde se ejecutará el login/token
def login(user: User):
    if user.email == "admin@gmail.com" and user.password == "admin":    #Habiendo definido las credenciales
        token:str = create_token(user.dict()) #Se llama a la funcion "create_token" y el servidor nos contesta con el token
        return JSONResponse(status_code=200, content=token)
