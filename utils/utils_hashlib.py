from passlib.context import CryptContext

context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def get_password_hash(value: str) -> str:
    hash_ = context.hash(value)
    return hash_


def verify_password(plain_password: str, hashed_password: str) -> bool:
    result = context.verify(plain_password, hashed_password)
    return result
