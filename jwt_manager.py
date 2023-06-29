from jwt import encode, decode

def create_token(data: dict) -> str:   #Funcion para crear token, se usa ese algortimo por default.
    token: str = encode(payload=data, key="my_secret_key", algorithm="HS256")
    return token

def validate_token(token:str) -> dict: #Funcion para validar/decodificar un token, es necesario tener la clave secreta.
    data:dict = decode(token, key="my_secret_key", algorithms=["HS256"])
    return data


