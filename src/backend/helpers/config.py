from pydantic import Field
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    # API
    backend_host: str = Field("", description="the name of the back end service")
    backend_port: int = Field(5005, description="the port on the backend service where i can find the API")
    db_url: str = Field("sqlite+pysqlite:///controller.sqlite", description="the db to cache to")
    protocol: str = Field("https", description="protocol used to connect to backend")

    # Auth
    tenant_id: str = Field("5d62e663-e965-436f-aa6b-e841aae8bf8b", description="the B2C Tenant id")
    # Frontend Auth
    frontend_client_id: str = Field("26bb9d3d-ef6c-4aa3-a761-9c7ed4d1439c", description="the client ID for web")
    auth_policy: str = Field("B2C_1_signin", description="the auth policy for b2c")
    auth_url: str = Field("https://igsfmssandboxb2c.b2clogin.com", description="the Auth Url for the B2C tenant")
    redirect_uri: str = Field("http://localhost:5000/", description="the redirect URI registered with the tenant")
    # Backend Auth
    backend_client_id: str = Field("c2cd3e60-62d2-4070-acd3-00f05b69f6a7", description="the client ID for the backend")
    backend_auth_scope: str = Field("c2cd3e60-62d2-4070-acd3-00f05b69f6a7/.default")
    backend_client_secret: str = Field(
        "enI2OFF+X3MwTEV5SUxTRXEtOHN3dTNHd2lvUHFMOFhrQ2Z6dmFISg==",
        description="secret for auth between backend fleet controller and api",
    )

    def make_auth_config_js(self) -> str:
        return f"""
const msalConfig = {{
    auth: {{
        clientId: '{self.frontend_client_id}',
        authority: '{self.auth_url}/{self.tenant_id}/{self.auth_policy}',
        knownAuthorities: ['{self.auth_url}'],
        redirectUri: '{self.redirect_uri}',
    }},
    cache: {{
        cacheLocation: 'sessionStorage',
        storeAuthStateInCookie: false
    }}
}};

const loginRequest = {{
    scopes: ['openid', 'profile']
}};
        """
