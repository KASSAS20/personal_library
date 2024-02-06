import time
from typing import Dict

import jwt

JWT_SECRET = 'secret_token'
JWT_ALGORITHM = 'HS256'


def token_response(token: str):
    return {
        "access_token": token
    }


def generate_jwt(password: str, login: str) -> Dict[str, str]:
    payload = {
        "login": login,
        "password": password,
        "expires": time.time() + 604800  # +1 неделя
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token_response(token)


def decode_jwt(token: str) -> dict | None:
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except Exception as _ex:
        print(_ex)
        return {}
