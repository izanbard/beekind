from fastapi import APIRouter, Depends, status
from typing import Annotated
from sqlmodel import Session, select


from src.backend.models import ApiaryList, get_session, Apiary
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
