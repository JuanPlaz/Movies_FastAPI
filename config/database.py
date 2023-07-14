import os
from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.ext.declarative import declarative_base #Sirve para manipular todas las tablas de la base de datos

sqlite_file_name = "../database.sqlite"
base_dir = os.path.dirname(os.path.realpath(__file__)) ##Lee el directorio actual del archivo.

database_url = f"sqlite:///{os.path.join(base_dir, sqlite_file_name)}"  ##Se crea URL de la base de datos. Join para unir ambas Urls.

engine = create_engine(database_url, echo=True)  ##Representa el motor de la base de datos

Session = sessionmaker(bind=engine)    ##Se crea sesión para conectarse a la base de datos.

Base = declarative_base()
