from typing import Annotated
from uuid import UUID, uuid4

from pydantic import computed_field
from sqlmodel import SQLModel, Field, Relationship

# from local files
from .user_to_org_link import UserToOrgLink


class OrganisationsBase(SQLModel):
    org_name: str = Field(
        ...,
        description="Display name of org",
        schema_extra={"examples": ["100 acre wood"]},
    )


class Organisations(OrganisationsBase, table=True):
    __tablename__ = "organisations"
    org_id: UUID = Field(
        default_factory=uuid4,
        description="Internal ID of org",
        schema_extra={"examples": [uuid4().hex]},
        primary_key=True,
    )
    users: list["Users"] = Relationship(back_populates="orgs", link_model=UserToOrgLink)  # noqa: F821


class OrganisationsCreate(OrganisationsBase):
    pass


class OrganisationsPublic(OrganisationsBase):
    org_id: UUID


class OrganisationsPublicWithUsers(OrganisationsPublic):
    users: list["UsersPublic"] = []  # noqa: F821


class OrganisationsList(SQLModel):
    orgs: list[OrganisationsPublic] = Field(description="List of organisations objects")

    @computed_field
    @property
    def count(self) -> Annotated[int, Field(description="Number of organisations", schema_extra={"examples": [1]})]:
        return len(self.orgs)
