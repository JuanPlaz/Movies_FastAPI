from fastapi import APIRouter
from fastapi import Path, Query, Depends
from fastapi.responses import JSONResponse

from typing import List

from config.database import Session
from models.movie import Movie as MovieModel
from fastapi.encoders import jsonable_encoder
from middlewares.jwt_bearer import JWTBearer
from services.movie import MovieService
from schemas.movie import Movie

movie_router = APIRouter()


@movie_router.get('/movies', tags=['Movies'], response_model=List[Movie], status_code=200, dependencies=[Depends(JWTBearer())])
def get_movies() -> List[Movie]:
    db = Session()
    result = MovieService(db).get_movies()
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

@movie_router.get('/movies/{id}', tags=['Movies'], response_model=Movie)
def get_movies_by_id(id: int = Path(ge=1, le=2000)) -> Movie:  ##Se solicita el id (entero) como variable obligatoria
    db = Session()
    result = MovieService(db).get_movie(id)
    
    if not result:
        return JSONResponse(status_code=404, content={'message': "No encontrado"})
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

"""                         #Se omite el ciclo For al usar el metodo filter
    for item in movies:
        if item["id"] == id:
            return JSONResponse(content=item)
    return JSONResponse(status_code=404, content=[])
"""
@movie_router.get('/movies/', tags=['Movies'], response_model=List[Movie]) ##Por Parametro Query
def get_movies_by_category(category: str = Query(min_length=3, max_length=15), year: str = Query(min_length=1, max_length=5)) -> List[Movie]:   #En este caso se filtra por categoria y por año, ambas obligatorias
    #return [ item for item in movies if item['category'] == category ]  ##Using list comprhensions
    db = Session()
    result = MovieService(db).get_movie_category(category,year)

    if not result:
        return JSONResponse(status_code=404, content={'message': "No encontrado"})
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

""" #Se omite el ciclo For al usar el metodo filter
    for item in movies:
        if (item["category"] == category) and (item["year"] == year):
            return JSONResponse(content=item)
    return "No hay pelis de este tipo"
    """

"""@movie_router.post('/movies', tags=['Create Movies'])    #Se solicitan todos los datos como body request, de esta forma se actualiza el diccionario de pelis:
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
@movie_router.post('/movies', tags=['Movies'], response_model=dict, status_code=201)   
def create_movies(movie: Movie) -> dict: #Ahora los datos vienen del constructor Movie.
   
    db = Session()
    MovieService(db).create_movie(movie)
    
    
    """
    #MovieModel(title=movie.title, overview=movie.overview, year=movie.year) #Primera forma de extraer los parametros 
    new_movie= MovieModel(**movie.dict())  #Se trae movie como dict y se extraen los atributos y se pasan como parametro usando **
    db.add(new_movie)   #Se agrega la nueva pelicula a la base de datos
    db.commit()     #Se actualiza/recarga la base de datos
    """
    #La siguiente linea se suspende, pues ya se está creando la nueva pelicula y se está agregando a la db.
    #movies.append(movie.dict()) #Como ahora se estan es añadiendo objetos de tipo Movie, se debe convertir a dict().
    return JSONResponse(status_code=201, content={"message": "Se ha registrado la pelicula exitosamente."})

"""@movie_router.put('/movies/{id}', tags=['Update Movies'])    #En pro de identificar solo una peli por el id, este se solicita de manera obligatoria, el resto de informacion se pasa por el body.
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
@movie_router.put('/movies/{id}', tags=['Movies'], response_model=dict, status_code=200)    #En pro de identificar solo una peli por el id, este se solicita de manera obligatoria, el resto de informacion se pasa por el body usando el constructor:
def update_movies(id: int, movie: Movie) -> dict:
    db = Session()
    result = MovieService(db).get_movie(id)
    ###result = db.query(MovieModel).filter(MovieModel.id == id).first()
    if not result:
        return JSONResponse(status_code=404, content={'message': "No encontrado"})

    MovieService(db).update_movie(id, movie)       #Para actualizar, se llama al servicio que se crea "MovieService"

    """
    result.title = movie.title
    result.overview = movie.overview
    result.year = movie.year
    result.rating = movie.rating
    result.category = movie.category
    db.commit()
"""
    return JSONResponse(status_code=200, content={"message": "Se ha modificado la pelicula exitosamente."})

"""for item in movies:  ##Ya no es necesario actualizar los items en ciclo, se actualizan usando como se ve previamente.
        if item["id"] == id:
            item["title"] = movie.title
            item["overview"] = movie.overview
            item["year"] = movie.year
            item["rating"] = movie.rating
            item["category"] = movie.category """
        

@movie_router.delete('/movies/{id}', tags=['Movies'], response_model=dict, status_code=200)
def delete_movies(id: int) -> dict:

    db = Session()
    result = db.query(MovieModel).filter(MovieModel.id == id).first() #Se verifica que el resultado buscado exista.
    
    if not result:
        return JSONResponse(status_code=404, content={'message': "No encontrado"})
    
    MovieService(db).delete_movie(id)
    return JSONResponse(status_code=200, content={"message": "Se ha eliminado la pelicula exitosamente."}) 

"""
    for item in movies:
        if item["id"] == id:
            movies.remove(item)
            return JSONResponse(status_code=200, content={"message": "Se ha eliminado la pelicula exitosamente."}) 
            
        return JSONResponse(status_code=404, content={'message': "No encontrado"})"""
    

