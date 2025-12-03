from __future__ import annotations

from datetime import datetime
from typing import List

from sqlalchemy import DateTime, Integer, func, String, Column, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Scuola(Base):
    __tablename__ = "scuole"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nome: Mapped[str] = mapped_column(String, index=True, nullable=False)
    tipo: Mapped[str] = mapped_column(String, index=True, nullable=False)
    descrizione: Mapped[str] = mapped_column(String, nullable=True)
    indirizzo: Mapped[str] = mapped_column(String, index=True, nullable=False)
    email: Mapped[str] = mapped_column(String, index=True, nullable=False)
    telefono: Mapped[str] = mapped_column(String, index=True, nullable=False)
    sito_web: Mapped[str] = mapped_column(String, index=True, nullable=True)
    id_citta: Mapped[int] = Column(Integer, ForeignKey("citta.id"))
    citta = relationship("Citta", back_populates="scuole")

    indirizzi: Mapped[List["Indirizzo"]] = relationship("Indirizzo", back_populates="scuola")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )
