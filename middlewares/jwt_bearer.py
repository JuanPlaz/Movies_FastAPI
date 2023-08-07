from fastapi.security import HTTPBearer
from fastapi import Request, HTTPException
from jwt_manager import create_token, validate_token


class JWTBearer(HTTPBearer):    #Funcion que sirve para acceder a la peticion del usuario (manejar autenticaciones)
    async def __call__(self, request: Request): #Se define como funcion asyncrona debido a que tarda un tiempo en responder. 
        auth = await super().__call__(request)  #Devolverá el token
        data = validate_token(auth.credentials) #Se llama la funcion de validacion
        if data['email'] != "admin@gmail.com":  #Se compara la data y se eleva una excepción
            raise HTTPException(status_code=403, detail="Invalid Credentials")
       