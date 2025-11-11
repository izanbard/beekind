from sqlmodel import create_engine, SQLModel, Session

from .contacts import Contacts, ContactsList  # noqa: F401

engine = None


def get_db_engine():
    global engine
    return engine


def set_db_engine(config):
    global engine
    if engine is not None:
        return
    engine = create_engine(
        config.db_url,
        echo=True,
    )


def get_session():
    session = Session(engine)
    yield session
    session.close()


def create_db_tables(eng):
    SQLModel.metadata.create_all(eng)
