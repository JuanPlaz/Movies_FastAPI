from fastapi import FastAPI, Body, Path, Query
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List

app = FastAPI()
app.title = "Mi aplicacion con FastAPI"
app.version = "0.0.1"

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

@app.get('/movies', tags=['Movies'], response_model=List[Movie], status_code=200)
def get_movies() -> List[Movie]:
    return JSONResponse(status_code=200, content=movies)

@app.get('/movies/{id}', tags=['Movies by Id'], response_model=Movie)
def get_movies_by_id(id: int = Path(ge=1, le=2000)) -> Movie:  ##Se solicita el id (entero) como variable obligatoria
    for item in movies:
        if item["id"] == id:
            return JSONResponse(content=item)
    return JSONResponse(status_code=404, content=[])

@app.get('/movies/', tags=['Movis by Category and Year'], response_model=List[Movie]) ##Por Parametro Query
def get_movies_by_category(category: str = Query(min_length=3, max_length=15), year: str = Query(min_length=1, max_length=5)) -> List[Movie]:   #En este caso se filtra por categoria y por año, ambas obligatorias
    #return [ item for item in movies if item['category'] == category ]  ##Using list comprhensions
    for item in movies:
        if (item["category"] == category) & (item["year"] == year):
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
@app.post('/movies', tags=['Create Movies'], response_model=dict, status_code=201)   
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
@app.put('/movies/{id}', tags=['Update Movies'], response_model=dict, status_code=200)    #En pro de identificar solo una peli por el id, este se solicita de manera obligatoria, el resto de informacion se pasa por el body usando el constructor:
def update_movies(id: int, movie: Movie) -> dict:
    for item in movies:
        if item["id"] == id:
            item["title"] = movie.title
            item["overview"] = movie.overview
            item["year"] = movie.year
            item["rating"] = movie.rating
            item["category"] = movie.category
            return JSONResponse(status_code=200, content={"message": "Se ha modificado la pelicula exitosamente."})
        

@app.delete('/movies/{id}', tags=['Delete Movies by Id'], response_model=dict, status_code=200)
def delete_movies(id: int) -> dict:
    for item in movies:
        if item["id"] == id:
            movies.remove(item)
            return JSONResponse(status_code=200, content={"message": "Se ha eliminado la pelicula exitosamente."})
    return "No hay pelis con este Id"
