from datetime import datetime

from sqlalchemy import Boolean, DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from .database import Base


class ApplicationSubmission(Base):
    __tablename__ = "application_submissions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(255), index=True)
    phone: Mapped[str] = mapped_column(String(50))
    organization: Mapped[str] = mapped_column(String(255))
    position: Mapped[str] = mapped_column(String(255))
    group_name: Mapped[str] = mapped_column(String(255))
    motive: Mapped[str] = mapped_column(Text)
    career: Mapped[str] = mapped_column(Text)
    start_date: Mapped[str] = mapped_column(String(100))
    available_days: Mapped[str] = mapped_column(String(255))
    note: Mapped[str] = mapped_column(Text)
    agreed_to_privacy: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
