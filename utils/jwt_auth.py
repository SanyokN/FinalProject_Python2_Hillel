import datetime as dt

import jwt
from fastapi import Request
from starlette.responses import RedirectResponse

import dao
from config import JWT_KEY
from database import User


def encode_jwt(payload_data: dict) -> str:
    encode_jwt_ = jwt.encode(payload=payload_data, key=JWT_KEY, algorithm="HS256")
    return encode_jwt_


def decode_jwt(encoded_jwt: str) -> dict:
    try:
        decoded_data = jwt.decode(
            jwt=encoded_jwt,
            key=JWT_KEY,
            algorithms=["HS256"],
        )
        return decoded_data
    except jwt.exceptions.ExpiredSignatureError:
        return {}
    except jwt.exceptions.InvalidSignatureError:
        return {}


def set_cookies_web(user, response: RedirectResponse) -> RedirectResponse:
    if not user:
        return response
    payload = {
        "sub": user.email,
        "exp": dt.datetime.utcnow() + dt.timedelta(seconds=30000),
        "iat": dt.datetime.utcnow(),
    }
    jwt_token = encode_jwt(payload)
    response.set_cookie("token_user_usanka", jwt_token)
    return response


def get_user_web(request: Request) -> User | None:
    token = request.cookies.get("token_user_usanka")
    if not token:
        return
    user_data = decode_jwt(token)
    if not user_data:
        return
    user = dao.get_user_by_email_dao(user_data["sub"])
    return user
