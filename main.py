from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel

from starlette.requests import Request
from utils.jwt_manager import create_token
from config.database import engine, Base 

from middlewares.error_handler import Error_Handler
from routers.movie import movie_router
from routers.user import user_router

app = FastAPI()
app.title = "Mi aplicacion con FastAPI"
app.version = "0.0.3"

app.add_middleware(Error_Handler)   #Se linkea el error handler creado anteriormente.
app.include_router(movie_router)    #Se linkea el router con los metodos relacionados con Movies.
app.include_router(user_router)     #Se linkea el router con el metodo post en User.

Base.metadata.create_all(bind= engine)

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

