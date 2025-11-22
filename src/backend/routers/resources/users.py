import uuid
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, status, Path, HTTPException
from sqlmodel import Session, select

from src.backend.auth import AuthHelper
from src.backend.models import Users, UsersList, Organisations, OrganisationsList, get_session

UserRouter = APIRouter(
    dependencies=[Depends(AuthHelper.bearer_token)],
    tags=["Users"],
    prefix="/users",
)


@UserRouter.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=UsersList,
    summary="Get list of all users",
    description="Get list of all users",
)
async def get_users_list(db: Annotated[Session, Depends(get_session)]) -> UsersList | None:
    users = db.scalars(select(Users)).all()
    return UsersList(users=users)


@UserRouter.get(
    "/{user_id}",
    status_code=status.HTTP_200_OK,
    response_model=Users | None,
    summary="Get a specific user",
    description="Get a specific user",
)
async def get_user_by_id(
    user_id: Annotated[UUID, Path(..., description="Internal ID of a user", example=str(uuid.uuid4()))],
    db: Annotated[Session, Depends(get_session)],
) -> type[Users | None]:
    user = db.get(Users, user_id)
    if user is not None:
        return user
    raise HTTPException(status_code=404, detail="No such User")


@UserRouter.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=Users,
    summary="Create a new user",
    description="Create a new user",
)
async def create_new_user(
    user: Users,
    db: Annotated[Session, Depends(get_session)],
) -> Users:
    with db.begin():
        if type(user.user_id) is str:
            user.user_id = UUID(str(user.user_id))
        db.merge(user)
    return user


@UserRouter.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete a user", description="Delete a user")
async def delete_user_by_id(
    user_id: Annotated[UUID, Path(..., description="Internal ID of a user", example=str(uuid.uuid4()))],
    db: Annotated[Session, Depends(get_session)],
) -> None:
    with db.begin():
        user = db.get(Users, user_id)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        db.delete(user)
    return None


@UserRouter.put(
    "/{user_id}/{org_id}",
    status_code=status.HTTP_200_OK,
    response_model=OrganisationsList,
    summary="Add a user to an org",
    description="Add a user to an org",
)
async def add_user_to_org(
    user_id: Annotated[UUID, Path(..., description="Internal ID of a user", example=str(uuid.uuid4()))],
    org_id: Annotated[UUID, Path(..., description="Internal ID of a org", example=str(uuid.uuid4()))],
    db: Annotated[Session, Depends(get_session)],
) -> OrganisationsList:
    with db.begin():
        user = db.get(Users, user_id)
        if user is None:
            raise HTTPException(status_code=404, detail="No User to add")
        org = db.get(Organisations, org_id)
        if org is None:
            raise HTTPException(status_code=404, detail="Organisation not found")
        org.users.append(user)
    return OrganisationsList(orgs=user.orgs)
