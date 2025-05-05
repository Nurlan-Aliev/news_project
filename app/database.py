from sqlalchemy.orm import (
    DeclarativeBase,
    sessionmaker,
    Mapped,
    mapped_column,
    declared_attr,
)
import sqlalchemy
from app.settings import settings


class Base(DeclarativeBase):
    @declared_attr.directive
    def __tablename__(cls):
        return f"{cls.__name__.lower()}"

    id: Mapped[int] = mapped_column(primary_key=True)


class DataBaseHelper:
    def __init__(self, path, echo=False):
        self.engine = sqlalchemy.create_engine(url=path, echo=echo)

        self.session_factory = sessionmaker(
            self.engine,
            autoflush=False,
            expire_on_commit=False,
            autocommit=False,
        )

    def session_depends(self):
        with self.session_factory() as session:
            yield session


db_helper = DataBaseHelper(
    settings.db_path,
    settings.DEBAG,
)
