from fastapi import FastAPI, Body, Path, Query, Request, HTTPException, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.security.http import HTTPAuthorizationCredentials
from pydantic import BaseModel, Field
from typing import Optional, List

from starlette.requests import Request

from jwt_manager import create_token, validate_token
from fastapi.security import HTTPBearer

from config.database import Session, engine, Base
from models.movie import Movie

app = FastAPI()
app.title = "Mi aplicacion con FastAPI"
app.version = "0.0.2"

Base.metadata.create_all(bind= engine)

class JWTBearer(HTTPBearer):    #Funcion que sirve para acceder a la peticion del usuario
    async def __call__(self, request: Request): #Se define como funcion asyncrona debido a que tarda un tiempo en responder. 
        auth = await super().__call__(request)  #Devolverá el token
        data = validate_token(auth.credentials) #Se llama la funcion de validacion
        if data['email'] != "admin@gmail.com":  #Se compara la data y se eleva una excepción
            raise HTTPException(status_code=403, detail="Invalid Credentials")
       
class User(BaseModel):
    email: str
    password: str

class Movie(BaseModel):
    #id: int | None = None   #La variable podria ser de tipo entero, o None porque podria ser una variable opcional.
    id: Optional[int] = None #Importando "Optional" de la libreria Typing, puedo volver la variable opcional como se observa.
    #title: str = Field(default="Mi pelicula", min_length=5, max_length=15) #Usando "default" se le puede dar un valor inicial a la variable.
    title: str = Field(min_length=5, max_length=15)
    overview: str = Field(min_length=15, max_length=50)
    year: int = Field(le=2023)
    rating: float = Field(ge=1, le=10)
    category: str = Field(min_length=5, max_length=15)

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "title": "Mi pelicula",
                "overview": "Descripción de la peli",
                "year": 1999,
                "rating": 9.9,
                "category": "Sci-fi"
            }
        }

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

@app.get('/movies', tags=['Movies'], response_model=List[Movie], status_code=200, dependencies=[Depends(JWTBearer())])
def get_movies() -> List[Movie]:
    return JSONResponse(status_code=200, content=movies)

@app.get('/movies/{id}', tags=['Movies'], response_model=Movie)
def get_movies_by_id(id: int = Path(ge=1, le=2000)) -> Movie:  ##Se solicita el id (entero) como variable obligatoria
    for item in movies:
        if item["id"] == id:
            return JSONResponse(content=item)
    return JSONResponse(status_code=404, content=[])

@app.get('/movies/', tags=['Movies'], response_model=List[Movie]) ##Por Parametro Query
def get_movies_by_category(category: str = Query(min_length=3, max_length=15), year: str = Query(min_length=1, max_length=5)) -> List[Movie]:   #En este caso se filtra por categoria y por año, ambas obligatorias
    #return [ item for item in movies if item['category'] == category ]  ##Using list comprhensions
    for item in movies:
        if (item["category"] == category) and (item["year"] == year):
            return JSONResponse(content=item)
    return "No hay pelis de este tipo"

"""@app.post('/movies', tags=['Create Movies'])    #Se solicitan todos los datos como body request, de esta forma se actualiza el diccionario de pelis:
def create_movies(id: int = Body(), title: str = Body(), overview: str = Body(), year: int = Body(), rating: float = Body(), category: str = Body()):
    movies.append({
        "id": id,
        "title": title,
        "overview": overview,
        "year": year,
        "rating": rating,
        "category": category
    })
    return movies"""
    
    #Al tener la clase Movie creada, el constructor nos ahorra lineas de codigo:
@app.post('/movies', tags=['Movies'], response_model=dict, status_code=201)   
def create_movies(movie: Movie) -> dict: #Ahora los datos vienen del constructor Movie.
    movies.append(movie.dict()) #Como ahora se estan es añadiendo objetos de tipo Movie, se debe convertir a dict().
    return JSONResponse(status_code=201, content={"message": "Se ha registrado la pelicula exitosamente."})

"""@app.put('/movies/{id}', tags=['Update Movies'])    #En pro de identificar solo una peli por el id, este se solicita de manera obligatoria, el resto de informacion se pasa por el body.
def update_movies(id: int, title: str = Body(), overview: str = Body(), year: int = Body(), rating: float = Body(), category: str = Body()):
    for item in movies:
        if item["id"] == id:
            item["title"] = title
            item["overview"] = overview
            item["year"] = year
            item["rating"] = rating
            item["category"] = category
            return movies
        """

#Para el caso del put, se modifica igualmente teniendo en cuenta el constructor Movie, pero el id al ser obligatorio, no se elimina de las variables solicitadas:
@app.put('/movies/{id}', tags=['Movies'], response_model=dict, status_code=200)    #En pro de identificar solo una peli por el id, este se solicita de manera obligatoria, el resto de informacion se pasa por el body usando el constructor:
def update_movies(id: int, movie: Movie) -> dict:
    for item in movies:
        if item["id"] == id:
            item["title"] = movie.title
            item["overview"] = movie.overview
            item["year"] = movie.year
            item["rating"] = movie.rating
            item["category"] = movie.category
            return JSONResponse(status_code=200, content={"message": "Se ha modificado la pelicula exitosamente."})
        

@app.delete('/movies/{id}', tags=['Movies'], response_model=dict, status_code=200)
def delete_movies(id: int) -> dict:
    for item in movies:
        if item["id"] == id:
            movies.remove(item)
            return JSONResponse(status_code=200, content={"message": "Se ha eliminado la pelicula exitosamente."})
    return "No hay pelis con este Id"
