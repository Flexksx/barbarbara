import os
from collections.abc import Iterator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql+psycopg://barbarbara:barbarbara@localhost:5432/barbarbara",
)

engine = create_engine(DATABASE_URL)
SessionFactory = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass


def get_session() -> Iterator[Session]:
    with SessionFactory() as session:
        yield session
