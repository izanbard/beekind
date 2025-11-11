from fastapi import APIRouter, Depends

from src.backend.auth import AuthHelper
from .contacts import ContactRouter

ResourceRouter = APIRouter(
    dependencies=[Depends(AuthHelper.bearer_token)],
    tags=["Entities"],
    prefix="/resource",
)

ResourceRouter.include_router(ContactRouter)
