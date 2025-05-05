from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


class Reaction(Base):
    news_id: Mapped[int] = mapped_column(
        ForeignKey("news.id", ondelete="CASCADE"),
        nullable=True,
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )

    post: Mapped["News"] = relationship(back_populates="reactions")
