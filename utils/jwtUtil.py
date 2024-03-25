from jose import jwt
import os

JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
JWT_ALGORITHM = os.getenv('JWT_ALGORITHM')


def create_jwt_token(data: dict):
    jwtToken = jwt.encode(data, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return jwtToken

def get_jwt_data(token: str):
    payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
    return payload