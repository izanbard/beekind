from contextlib import asynccontextmanager
from io import StringIO
from typing import AsyncIterator, Annotated
from uuid import UUID

from fastapi import FastAPI, Response, Request, status, Depends
from fastapi.responses import JSONResponse
from sqlalchemy import delete
from sqlmodel import Session
from yaml import dump as yaml_dump

from src.backend.auth import MSAuthAdapter
from src.backend.helpers import get_logger, get_config
from src.backend.models import get_session, Users, Organisations, Contacts, UserToOrgLink, Apiary
from src.backend.routers import ResourceRouter


@asynccontextmanager
async def app_lifespan_startup_and_shutdown(app: FastAPI) -> AsyncIterator[None]:
    # before app is created
    config = get_config()
    MSAuthAdapter(config.frontend_client_id, config.tenant_id, config.auth_policy, config.auth_url)
    # yield to the app
    yield
    # after the app shuts down


def create_api() -> FastAPI:
    app_logger = get_logger()
    with open("version.txt") as f:
        version = f.readline().strip()
    tags_metadata = [
        {"name": "Resources", "description": "CRUD operations for the base data entities"},
        {"name": "Contacts", "description": "CRUD operations for the base contact entities", "parent": "Resources"},
        {"name": "Users", "description": "CRUD operations for the base user entities", "parent": "Resources"},
        {"name": "Organisations", "description": "CRUD operations for the base org entities", "parent": "Resources"},
        {"name": "Apiaries", "description": "CRUD operations for the base apiary entities", "parent": "Resources"},
    ]
    app_logger.info(f"Creating the app... version: {version}")
    app = FastAPI(
        title="BeeKind backend",
        openapi_url="/openapi.json",
        version=version,
        openapi_tags=tags_metadata,
        external_docs={"description": "Yaml API Spec", "url": "/openapi.yaml"},
        lifespan=app_lifespan_startup_and_shutdown,
    )

    app.include_router(ResourceRouter)

    @app.get(
        "/openapi.yaml",
        status_code=200,
        response_class=Response,
        include_in_schema=False,
    )
    async def yaml_spec() -> Response:
        spec_str = StringIO()
        yaml_dump(app.openapi(), spec_str, sort_keys=False)
        return Response(spec_str.getvalue(), media_type="text/yaml")

    @app.get("/populate", status_code=status.HTTP_201_CREATED, response_model=None, include_in_schema=False)
    async def populate(session: Annotated[Session, Depends(get_session)]) -> None:
        session.exec(delete(Users))
        session.exec(delete(Organisations))
        session.exec(delete(Contacts))
        session.exec(delete(UserToOrgLink))
        session.exec(delete(Apiary))
        session.commit()
        session.begin()
        user = Users(
            user_id=UUID("12345678-1234-1234-1234-123456789012"),
            username="Christopher Robin",
        )
        session.add(user)
        org = Organisations(
            org_id=UUID("12345678-1234-1234-1234-123456789012"),
            org_name="100 Aker Wood",
        )
        org.users.append(user)
        session.add(org)
        contact = Contacts(
            contact_id=UUID("12345678-1234-1234-1234-123456789012"),
            name="Winnie the Pooh",
            phone="+4411234567890",
            email="winnie@hundredaker.com",
            address="Pooh Corner, High St Hartfield, East Sussex, TN7 4AE",
            contact_notes="Only call late in the morning after Winne has had time to wake up. Piglet or tigger may answer.",
        )
        session.add(contact)
        apiary = Apiary(
            apiary_id=UUID("12345678-1234-1234-1234-123456789012"),
            site_lat=51.87419,
            site_lon=-1.18561,
            name="Pooh Corner",
            apiary_notes="Watch out for the large tree in the middle",
        )
        apiary.contact = contact
        apiary.organisation = org
        session.add(apiary)
        session.commit()
        return None

    app.add_exception_handler(status.HTTP_500_INTERNAL_SERVER_ERROR, internal_exception_handler)
    app_logger.info("App created")
    return app


def internal_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    content = {
        "code": 500,
        "msg": "Internal Server Error",
        "type": type(exc).__name__,
        "detail": str(exc),
    }
    app_logger = get_logger()
    app_logger.warning(
        f"Returning 500 due to exception: {type(exc).__name__}, {str(exc)}, for {request.method} to {request.url}"
    )
    return JSONResponse(
        status_code=500,
        content=content,
    )
