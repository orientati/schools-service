from __future__ import annotations

from sqlalchemy import String, Integer, Table, Column, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

indirizzi_materie_table = Table(
    "association_table",
    Base.metadata,
    Column("indirizzo_id", ForeignKey("indirizzi.id"), primary_key=True),
    Column("materia_id", ForeignKey("materie.id"), primary_key=True),
)


class Indirizzo(Base):
    __tablename__ = "indirizzi"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nome: Mapped[str] = mapped_column(String, index=True, nullable=False)
    descrizione: Mapped[str] = mapped_column(String, nullable=True)
    id_scuola: Mapped[int] = Column(Integer, ForeignKey("Scuole.id"))
    materie = relationship("Materie", secondary=indirizzi_materie_table)
    scuola = relationship("Scuole", back_populates="indirizzi")
