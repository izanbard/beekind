from typing import Annotated
from uuid import UUID, uuid4

from pydantic import computed_field
from sqlmodel import Field, SQLModel, Relationship


class ContactsBase(SQLModel):
    name: str = Field(
        ...,
        description="Name of the Contact",
        schema_extra={"examples": ["Winnie the Pooh"]},
    )
    phone: str | None = Field(
        None,
        description="Phone number of the Contact",
        schema_extra={"examples": ["+441234567890"]},
    )
    email: str | None = Field(
        None,
        description="Email address of the Contact",
        schema_extra={"examples": ["winnie@hundredaker.com"]},
    )
    address: str | None = Field(
        None,
        description="Address of the Contact",
        schema_extra={"examples": ["Pooh Corner, High St Hartfield, East Sussex, TN7 4AE"]},
    )
    contact_notes: str | None = Field(
        None,
        description="Notes about the Contact",
        schema_extra={
            "examples": [
                "Only call late in the morning after Winne has had time to wake up. Piglet or tigger may answer the phone."
            ]
        },
    )


class Contacts(ContactsBase, table=True):
    __tablename__ = "contacts"

    contact_id: UUID = Field(
        default_factory=uuid4,
        description="Internal ID of Contact",
        schema_extra={"examples": ["12345678-1234-1234-1234-123456789012"]},
        primary_key=True,
    )

    apiaries: list["Apiary"] = Relationship(back_populates="contact")  # noqa: F821


class ContactsCreate(ContactsBase):
    pass


class ContactsPublic(ContactsBase):
    contact_id: UUID = Field(
        ...,
        description="Internal ID of Contact",
        schema_extra={"examples": ["12345678-1234-1234-1234-123456789012"]},
    )


class ContactsPublicWithApiaries(ContactsPublic):
    apiaries: list["ApiaryPublic"] = []  # noqa: F821


class ContactsList(SQLModel):
    contacts: list[ContactsPublic] = Field(description="List of Contacts objects")

    @computed_field
    @property
    def count(self) -> Annotated[int, Field(description="Number of contacts", schema_extra={"examples": [1]})]:
        return len(self.contacts)
