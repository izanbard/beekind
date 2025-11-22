from fastapi import APIRouter, Depends

from src.backend.auth import AuthHelper
from src.backend.routers.resources import ContactRouter, UserRouter, OrgRouter

ResourceRouter = APIRouter(
    dependencies=[Depends(AuthHelper.bearer_token)],
    prefix="/resource",
)

ResourceRouter.include_router(ContactRouter)
ResourceRouter.include_router(UserRouter)
ResourceRouter.include_router(OrgRouter)
