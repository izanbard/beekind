from sqlmodel import SQLModel, Field


class Token(SQLModel):
    token_type: str = Field(..., description="the Token type", schema_extra={"examples": ["Bearer"]})
    access_token: str = Field(
        ...,
        description="The JWT for Accessing the API",
        schema_extra={"examples": ["eyXXXX.eyYYYY.eyZZZZ"]},
    )
    expires_in: int = Field(..., gt=0, description="Expiration time in .", schema_extra={"examples": [300]})
    refresh_token: str = Field(
        ...,
        description="The JWT for Refreshing the Access Token",
        schema_extra={"examples": ["eyXXXX.eyYYYY.eyZZZZ"]},
    )
    refresh_expires_in: int = Field(
        ..., gt=0, description="Refresh Expiration time in seconds.", schema_extra={"examples": [1800]}
    )


class Credentials(SQLModel):
    username: str = Field(..., description="The username of the user", schema_extra={"examples": ["crobin"]})
    password: str = Field(..., description="The password of the user", schema_extra={"examples": ["<<PASSWORD>>"]})
