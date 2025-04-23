from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[bytes]
    first_name: Mapped[str]
    last_name: Mapped[str]
    status: Mapped[str]
    news: Mapped[List["News"]] = relationship(
        back_populates="user", passive_deletes=True
    )
