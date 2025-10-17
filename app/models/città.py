from __future__ import annotations

from typing import List

from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Citta(Base):
    __tablename__ = "citta"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nome: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    provincia: Mapped[str] = mapped_column(String, index=True, nullable=False)
    codice_postale: Mapped[str] = mapped_column(String, index=True, nullable=False)
    scuole: Mapped[List["Scuola"]] = relationship("Scuola", back_populates="citta")
