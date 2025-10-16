from __future__ import annotations

from datetime import datetime
from sqlalchemy import String, DateTime, Integer, func
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base


class Materia(Base):
    __tablename__ = "materie"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nome: Mapped[str] = mapped_column(String, index=True, nullable=False)
    descrizione: Mapped[str] = mapped_column(String, nullable=True)

