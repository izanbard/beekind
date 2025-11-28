from typing import Annotated

from fastapi import HTTPException, status, Depends, Cookie
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jwcrypto.jwt import JWTExpired
from keycloak import KeycloakOpenID, KeycloakError


from src.backend.helpers import Config, get_config


class AuthHelper:
    @staticmethod
    def get_token():
        return HTTPBearer()

    @staticmethod
    def get_keycloak_client(config: Annotated[Config, Depends(get_config)]):
        keycloak_client = KeycloakOpenID(
            server_url=config.base_auth_url,
            realm_name=config.realm,
            client_id=config.backend_client_id,
            client_secret_key=config.backend_client_secret,
            verify=False,
        )
        return keycloak_client

    @staticmethod
    def bearer_token(
        token_client: Annotated[KeycloakOpenID, Depends(get_keycloak_client)],
        token: Annotated[HTTPAuthorizationCredentials, Depends(get_token())],
    ) -> dict:
        if token.credentials is None or token.credentials == "":
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token")
        if token.scheme != "Bearer":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Auth header must be Bearer Token",
            )
        decoded_token = AuthHelper.validate_token(token, token_client)
        return decoded_token

    @staticmethod
    def cookie_token(
        token_client: Annotated[KeycloakOpenID, Depends(get_keycloak_client)],
        authorization: Annotated[str, Cookie()] = None,
    ) -> dict:
        if authorization is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        if authorization is not None and authorization.startswith("Bearer "):
            authorization = authorization.split(" ")[1]
        token: HTTPAuthorizationCredentials = HTTPAuthorizationCredentials(
            scheme="Bearer",
            credentials=authorization,
        )
        decode_token = AuthHelper.validate_token(token, token_client)
        return decode_token

    @staticmethod
    def validate_token(token: HTTPAuthorizationCredentials, kc_client: KeycloakOpenID) -> dict | None:
        try:
            decoded_token = kc_client.decode_token(token.credentials)
        except (KeycloakError, ValueError, JWTExpired) as e:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
        return decoded_token
