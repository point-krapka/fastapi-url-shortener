from __future__ import annotations

from sqlalchemy import Boolean, DateTime, Integer, String, func,ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from app.infrastructure.db.models.base import Base

class Link(Base):
    __tablename__ = "links"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    short_url: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    origin_url: Mapped[str] = mapped_column(String, nullable=False)
    count_visits: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship(back_populates="links")

    visits: Mapped[list["Visit"]] = relationship(back_populates="link")