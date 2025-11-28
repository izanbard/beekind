from pydantic import Field
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    # API
    db_url: str = Field("sqlite+pysqlite:///controller.sqlite", description="the db to cache to")

    # Auth
    realm: str = Field("beekind", description="the B2C Tenant id")
    base_auth_url: str = Field("https://rednodepi.local.net:5001/", description="the Auth Url for the B2C tenant")
    token_endpoint: str = Field("protocol/openid-connect/token", description="the endpoint for the OIDC token")
    # Frontend Auth
    frontend_client_id: str = Field("26bb9d3d-ef6c-4aa3-a761-9c7ed4d1439c", description="the client ID for web")
    auth_policy: str = Field("B2C_1_signin", description="the auth policy for b2c")
    # Backend Auth
    backend_client_id: str = Field("backend-client", description="client ID")
    backend_client_secret: str = Field("qoLSiYoYzIQgyLuX9TUCZLziqe1vbn3i", description="client secret")
