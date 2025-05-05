from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


class Users(Base):
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[bytes]
    first_name: Mapped[str]
    last_name: Mapped[str]
    role: Mapped[str] = mapped_column(default="user")
    news: Mapped[List["News"]] = relationship(
        back_populates="user", passive_deletes=True
    )
