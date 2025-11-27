from decimal import Decimal
from typing import Annotated
from uuid import UUID, uuid4

from pydantic import computed_field
from sqlmodel import SQLModel, Field, Relationship

from . import Organisations, Contacts


class ApiaryBase(SQLModel):
    org_id: UUID | None = Field(
        default=None,
        description="Organization ID",
        schema_extra={"examples": ["12345678-1234-1234-1234-123456789012"]},
        foreign_key="organisations.org_id",
    )
    contact_id: UUID | None = Field(
        default=None,
        description="Contact ID",
        schema_extra={"examples": ["12345678-1234-1234-1234-123456789012"]},
        foreign_key="contacts.contact_id",
    )
    site_lat: Decimal = Field(
        default=0,
        max_digits=9,
        decimal_places=7,
        description="Site latitude",
        schema_extra={"examples": [51.8741900]},
    )
    site_lon: Decimal = Field(
        default=0,
        max_digits=10,
        decimal_places=7,
        description="Site longitude",
        schema_extra={"examples": [-1.1856100]},
    )
    name: str = Field(
        ...,
        description="Name of the Apiary",
        schema_extra={"examples": ["Pooh Corner"]},
    )
    apiary_notes: str | None = Field(
        None,
        description="Notes about the Apiary",
        schema_extra={"examples": ["Watch out for the large tree in the middle"]},
    )


class Apiary(ApiaryBase, table=True):
    __tablename__ = "apiary"
    apiary_id: UUID = Field(
        default_factory=uuid4,
        description="Internal ID of Apiary",
        schema_extra={"examples": ["12345678-1234-1234-1234-123456789012"]},
        primary_key=True,
    )
    contact: Contacts | None = Relationship(back_populates="apiaries")
    organisation: Organisations | None = Relationship(back_populates="apiaries")


class ApiaryCreate(ApiaryBase):
    pass


class ApiaryPublic(ApiaryBase):
    apiary_id: UUID = Field(
        ...,
        description="Internal ID of Contact",
        schema_extra={"examples": ["12345678-1234-1234-1234-123456789012"]},
    )


class ApiaryPublicWithContact(ApiaryPublic):
    contact: type["ContactsPublic"] | None = None  # noqa: F821


class ApiaryList(SQLModel):
    apiaries: list[ApiaryPublic] = Field(description="List of Apiary objects")

    @computed_field
    @property
    def count(self) -> Annotated[int, Field(description="Number of apiaries", schema_extra={"examples": [1]})]:
        return len(self.apiaries)
