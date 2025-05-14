from typing import Optional
from app.news.likes.models import Reaction
from sqlalchemy import ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base
from app.news.enums import Status


class News(Base):

    title: Mapped[str]
    content: Mapped[str]
    status: Mapped[Status] = mapped_column(Enum(Status), default=Status.pending)
    user_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL")
    )
    user: Mapped["Users"] = relationship(back_populates="news")
    reactions: Mapped[list["Reaction"]] = relationship(back_populates="post")
