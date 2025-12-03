from __future__ import annotations

from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.indirizzo import indirizzi_materie_table


class Materia(Base):
    __tablename__ = "materie"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nome: Mapped[str] = mapped_column(String, index=True, nullable=False)
    descrizione: Mapped[str] = mapped_column(String, nullable=True)
    indirizzi = relationship("Indirizzo", secondary=indirizzi_materie_table, back_populates="materie")
