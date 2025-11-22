import uuid
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, status, Path, HTTPException
from sqlmodel import Session, select

from src.backend.auth import AuthHelper
from src.backend.models import Contacts, ContactsList, get_session

ContactRouter = APIRouter(
    dependencies=[Depends(AuthHelper.bearer_token)],
    tags=["Contacts"],
    prefix="/contacts",
)


@ContactRouter.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=ContactsList,
    summary="Get list of all all contacts",
    description="Get list of all all contacts",
)
async def get_contacts_list(
    db: Annotated[Session, Depends(get_session)],
) -> ContactsList | None:
    contacts = db.scalars(select(Contacts)).all()
    return ContactsList(contacts=contacts)


@ContactRouter.get(
    "/{contact_id}",
    status_code=status.HTTP_200_OK,
    response_model=Contacts | None,
    summary="Get a specific contact",
    description="Get a specific contact",
)
async def get_contact_by_id(
    contact_id: Annotated[UUID, Path(..., description="Internal ID of a contact", example=str(uuid.uuid4()))],
    db: Annotated[Session, Depends(get_session)],
) -> type[Contacts | None]:
    contact = db.get(Contacts, contact_id)
    if contact is not None:
        return contact
    raise HTTPException(status_code=404, detail="Contact not found")


@ContactRouter.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=Contacts,
    summary="Create a new contact",
    description="Create a new contact",
)
async def create_new_contact(
    contact: Contacts,
    db: Annotated[Session, Depends(get_session)],
) -> Contacts:
    with db.begin():
        if type(contact.id) is str:
            contact.id = UUID(str(contact.id))
        db.merge(contact)
    return contact


@ContactRouter.delete(
    "/{contact_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete a contact", description="Delete a contact"
)
async def delete_contact_by_id(
    contact_id: Annotated[UUID, Path(..., description="Internal ID of a contact", example=str(uuid.uuid4()))],
    db: Annotated[Session, Depends(get_session)],
) -> None:
    with db.begin():
        contact = db.get(Contacts, contact_id)
        if contact is None:
            raise HTTPException(status_code=404, detail="Contact not found")
        db.delete(contact)
    return None
