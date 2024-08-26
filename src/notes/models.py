from sqlalchemy import Integer, String, ForeignKey, DateTime, text
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime
from ..auth.models import Base

class Note(Base):
    __tablename__ = "notes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    content: Mapped[str] = mapped_column(String(length=320), index=True, nullable=False)
    creator_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=text("TIMEZONE('utc', now())")
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=text("TIMEZONE('utc', now())"),
        onupdate=text("TIMEZONE('utc', now())"),
    )

    creator = relationship("User", back_populates="notes")

    def __repr__(self) -> str:
        return f"<Note(id={self.id}, content='{self.content[:50]}...')>"