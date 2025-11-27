from typing import Annotated
from uuid import UUID, uuid4

from pydantic import computed_field
from sqlmodel import SQLModel, Field, Relationship

# from local files
from .user_to_org_link import UserToOrgLink


class UsersBase(SQLModel):
    username: str = Field(
        ...,
        description="Display name of User",
        schema_extra={"examples": ["Christopher Robin"]},
    )


class Users(UsersBase, table=True):
    __tablename__ = "users"
    user_id: UUID = Field(
        default_factory=uuid4,
        description="Internal ID of User",
        schema_extra={"examples": ["12345678-1234-1234-1234-123456789012"]},
        primary_key=True,
    )

    orgs: list["Organisations"] = Relationship(back_populates="users", link_model=UserToOrgLink)  # noqa: F821


class UsersCreate(UsersBase):
    pass


class UsersPublic(UsersBase):
    user_id: UUID = Field(
        ...,
        description="Internal ID of User",
        schema_extra={"examples": ["12345678-1234-1234-1234-123456789012"]},
    )


class UsersPublicWithOrgs(UsersPublic):
    orgs: list["OrganisationsPublic"] = []  # noqa: F821


class UsersList(SQLModel):
    users: list[UsersPublic] = Field(description="List of Users objects")

    @computed_field
    @property
    def count(self) -> Annotated[int, Field(description="Number of users", schema_extra={"examples": [1]})]:
        return len(self.users)
