from models.movie import Movie as MovieModel

class MovieService():

    def __init__(self, db) -> None: #Cuando se llame este servicio, se le envía una sesión a la Base de datos (db).
        self.db = db

    def get_movies(self):
        result = self.db.query(MovieModel).all()
        return result
    
    def get_movie(self, id):
        result = self.db.query(MovieModel).filter(MovieModel.id == id).first()
        return result
    
    def get_movie_category(self, category, year):
        result = self.db.query(MovieModel).filter(MovieModel.category == category and MovieModel.year == year).all()
        return result