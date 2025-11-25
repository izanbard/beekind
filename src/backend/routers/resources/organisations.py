import uuid
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, status, Path, HTTPException
from sqlmodel import Session, select

from src.backend.auth import AuthHelper
from src.backend.models import (
    Organisations,
    OrganisationsList,
    Users,
    get_session,
    OrganisationsPublic,
    OrganisationsCreate,
    OrganisationsPublicWithUsers,
)

OrgRouter = APIRouter(
    dependencies=[Depends(AuthHelper.bearer_token)],
    tags=["Organisations"],
    prefix="/orgs",
)


@OrgRouter.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=OrganisationsList,
    summary="Get list of all orgs",
    description="Get list of all orgs",
)
async def get_organisations_list(
    db: Annotated[Session, Depends(get_session)],
) -> OrganisationsList | None:
    orgs = db.scalars(select(Organisations)).all()
    return OrganisationsList(orgs=orgs)


@OrgRouter.get(
    "/{org_id}",
    status_code=status.HTTP_200_OK,
    response_model=OrganisationsPublicWithUsers | None,
    summary="Get a specific org",
    description="Get a specific org",
)
async def get_organisation_by_id(
    org_id: Annotated[UUID, Path(..., description="Internal ID of a org", example=str(uuid.uuid4()))],
    db: Annotated[Session, Depends(get_session)],
) -> type[Organisations | None]:
    org = db.get(Organisations, org_id)
    if org is not None:
        return org
    raise HTTPException(status_code=404, detail="Org not found")


@OrgRouter.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=OrganisationsPublic,
    summary="Create a new org",
    description="Create a new org",
)
async def create_new_organisation(
    organisation: OrganisationsCreate,
    db: Annotated[Session, Depends(get_session)],
) -> Organisations:
    with db.begin():
        db_org = Organisations.model_validate(organisation)
        db.add(db_org)
    db.refresh(db_org)
    return db_org


@OrgRouter.delete("/{org_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete an org", description="Delete an org")
async def delete_organisation_by_id(
    org_id: Annotated[UUID, Path(..., description="Internal ID of a org", example=str(uuid.uuid4()))],
    db: Annotated[Session, Depends(get_session)],
) -> None:
    with db.begin():
        user = db.get(Organisations, org_id)
        if user is None:
            raise HTTPException(status_code=404, detail="Org not found")
        db.delete(user)
    return None


@OrgRouter.put(
    "/{org_id}/{user_id}",
    status_code=status.HTTP_200_OK,
    response_model=OrganisationsPublicWithUsers,
    summary="Add a user to an org",
    description="Add a user to an org",
)
async def add_user_to_org(
    user_id: Annotated[UUID, Path(..., description="Internal ID of a user", example=str(uuid.uuid4()))],
    org_id: Annotated[UUID, Path(..., description="Internal ID of a org", example=str(uuid.uuid4()))],
    db: Annotated[Session, Depends(get_session)],
) -> type[Organisations]:
    with db.begin():
        org = db.get(Organisations, org_id)
        if org is None:
            raise HTTPException(status_code=404, detail="Organisation not found")
        user = db.get(Users, user_id)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        user.orgs.append(org)
    db.refresh(org)
    return org
