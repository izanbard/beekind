from typing import Annotated

from fastapi import HTTPException, status, Depends, Cookie
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jwt import PyJWTError

from src.backend.auth.ms_auth_adapter import MSAuthAdapter


class AuthHelper:
    @staticmethod
    def get_token():
        return HTTPBearer()

    @staticmethod
    def bearer_token(token: Annotated[HTTPAuthorizationCredentials, Depends(get_token())]) -> (bool, str | dict | PyJWTError):
        if token.scheme != "Bearer":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Auth header must be Bearer Token",
            )
        if token.credentials is None or token.credentials == "":
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token")
        valid, msg = AuthHelper.validate_token(token.credentials)
        if not valid:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=msg)
        return valid, msg

    @staticmethod
    def cookie_token(authorization: Annotated[str, Cookie()] = None) -> bool:
        if authorization is not None and authorization.startswith("Bearer "):
            authorization = authorization[7:]
        if authorization is None:
            return False
        valid, msg = AuthHelper.validate_token(authorization)
        if not valid:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=msg)
        return valid

    @staticmethod
    def validate_token(token):
        ms_auth = MSAuthAdapter.get_singleton_instance()
        valid, msg = ms_auth.decode_token(token)
        return valid, msg
