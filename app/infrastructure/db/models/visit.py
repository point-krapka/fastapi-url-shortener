from sqlalchemy import Boolean, DateTime, Integer, String, func,ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from . import Base,Link
class Visit(Base):
    __tablename__ = "visits"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_agent: Mapped[str | None] = mapped_column(String, nullable=True)
    ip_address: Mapped[str | None] = mapped_column(String, nullable=True)
    os: Mapped[str | None] = mapped_column(String, nullable=True)
    browser: Mapped[str | None] = mapped_column(String, nullable=True)
    device: Mapped[str | None] = mapped_column(String, nullable=True)
    language: Mapped[str | None] = mapped_column(String, nullable=True)
    timezone: Mapped[str | None] = mapped_column(String, nullable=True)
    size_window: Mapped[str | None] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    link_id: Mapped[int] = mapped_column(ForeignKey("links.id"))
    link: Mapped["Link"] = relationship(back_populates="visits")