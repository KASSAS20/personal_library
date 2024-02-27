import bcrypt
import jwt


# Функция для хеширования пароля с добавлением соли
def get_hashed_password(plain_text_password: str) -> bytes:
    return bcrypt.hashpw(plain_text_password.encode(), bcrypt.gensalt())


# сравнение пароля с хэшированным паролем из бд
def check_password(plain_text_password: str, hashed_password: bytes) -> bool:
    return bcrypt.checkpw(plain_text_password.encode(), hashed_password)


# генерация JWT
def get_jwt(data: dict, key: str) -> str:
    jwt_token = jwt.encode(data, key, algorithm='HS256')
    return jwt_token


# Декодирование JWT
def jwt_decode(token: dict, key: str) -> dict:
    return jwt.decode(jwt=token, key=key, algorithms='HS256')
