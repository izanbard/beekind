from typing import Annotated, Generator

from fastapi.params import Depends
from sqlalchemy import Engine
from sqlmodel import create_engine, SQLModel, Session


from src.backend.helpers import Config, get_config

# from local files
from .contacts import Contacts, ContactsList  # noqa: F401
from .organisations import Organisations, OrganisationsList  # noqa: F401
from .users import Users, UsersList  # noqa: F401
from .user_to_org_link import UserToOrgLink  # noqa: F401

engine = None


def get_db_engine(config: Annotated[Config, Depends(get_config)]) -> Engine:
    global engine
    if engine is not None:
        return engine
    engine = create_engine(
        config.db_url,
        echo=True,
    )
    create_db_tables(engine)
    return engine


def get_session(db_engine: Annotated[Engine, Depends(get_db_engine)]) -> Generator[Session, None, None]:
    session = Session(db_engine)
    yield session
    session.close()


def create_db_tables(eng) -> None:
    SQLModel.metadata.create_all(eng)
