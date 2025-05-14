from typing import Optional

from app.news.likes.models import Reaction
from app.settings import settings
from sqlalchemy import ForeignKey, select, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


class News(Base):

    title: Mapped[str]
    content: Mapped[str]
    status: Mapped[str] = mapped_column(default=settings.news_status["pending"])
    user_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL")
    )
    user: Mapped["Users"] = relationship(back_populates="news")

    reactions: Mapped[list["Reaction"]] = relationship(back_populates="post")
