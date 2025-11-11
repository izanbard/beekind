from io import StringIO

from fastapi import FastAPI, Response, Request, status
from fastapi.responses import JSONResponse
from yaml import dump as yaml_dump

from . import get_logger
from .routers import ResourceRouter


def create_api():
    app_logger = get_logger()
    with open("version.txt") as f:
        version = f.readline()
    tags_metadata = [
        {"name": "Entities", "description": "CRUD operations for the base data entities"},
    ]
    app_logger.info(f"Creating the app... version: {version}")
    app = FastAPI(
        title="BeeKind backend",
        openapi_url="/openapi.json",
        version=version,
        openapi_tags=tags_metadata,
        external_docs={"description": "Yaml API Spec", "url": "/openapi.yaml"},
    )
    app.include_router(ResourceRouter)

    @app.get(
        "/openapi.yaml",
        status_code=200,
        response_class=Response,
        include_in_schema=False,
    )
    async def yaml_spec():
        spec_str = StringIO()
        yaml_dump(app.openapi(), spec_str, sort_keys=False)
        return Response(spec_str.getvalue(), media_type="text/yaml")

    app.add_exception_handler(status.HTTP_500_INTERNAL_SERVER_ERROR, internal_exception_handler)
    app_logger.info("App created")
    return app


def internal_exception_handler(request: Request, exc: Exception):
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
