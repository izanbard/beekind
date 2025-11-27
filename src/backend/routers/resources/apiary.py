from uuid import UUID

from fastapi import APIRouter, Depends, status, HTTPException, Path
from typing import Annotated
from sqlmodel import Session, select

from src.backend.models import ApiaryList, get_session, Apiary, ApiaryPublic, ApiaryCreate
from src.backend.auth import AuthHelper

ApiaryRouter = APIRouter(
    dependencies=[Depends(AuthHelper.bearer_token)],
    tags=["Apiaries"],
    prefix="/apiary",
)


@ApiaryRouter.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=ApiaryList,
    summary="Get list of all Apiaries",
    description="Get list of all Apiaries",
)
async def get_apiary_list(
    db: Annotated[Session, Depends(get_session)],
) -> ApiaryList | None:
    apiaries = db.scalars(select(Apiary)).all()
    return ApiaryList(apiaries=apiaries)


@ApiaryRouter.get(
    "/{apiary_id}",
    status_code=status.HTTP_200_OK,
    response_model=ApiaryPublic | None,
    summary="Get a specific Apiary",
    description="Get a specific Apiary",
)
async def get_apiary_by_id(
    apiary_id: Annotated[UUID, Path(..., description="Internal of an Apiary", example="12345678-1234-1234-1234-123456789012")],
    db: Annotated[Session, Depends(get_session)],
) -> type[Apiary | None]:
    apiary = db.get(Apiary, apiary_id)
    if apiary is not None:
        return apiary
    raise HTTPException(status_code=404, detail="Apiary not found")


@ApiaryRouter.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=ApiaryPublic,
    summary="Create a new Apiary",
    description="Create a new Apiary",
)
async def create_apiary(
    apiary: ApiaryCreate,
    db: Annotated[Session, Depends(get_session)],
) -> Apiary:
    with db.begin():
        db_apiary = Apiary.model_validate(apiary)
        db.add(db_apiary)
    db.refresh(db_apiary)
    return db_apiary


@ApiaryRouter.delete(
    "/{apiary_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a specific Apiary",
    description="Delete a specific Apiary",
)
async def delete_apiary_by_id(
    apiary_id: Annotated[UUID, Path(..., description="Internal of an Apiary", example="12345678-1234-1234-1234-123456789012")],
    db: Annotated[Session, Depends(get_session)],
) -> None:
    with db.begin():
        db_apiary = db.get(Apiary, apiary_id)
        if db_apiary is None:
            raise HTTPException(status_code=404, detail="Apiary not found")
        db.delete(db_apiary)
    return None
