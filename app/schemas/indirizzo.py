from __future__ import annotations

from typing import List

from pydantic import BaseModel


class IndirizzoBase(BaseModel):
    nome: str
    descrizione: str | None = None
    id_scuola: int


class IndirizzoResponse(IndirizzoBase):
    id: int | None = None


class IndirizzoCreate(IndirizzoBase):
    pass


class IndirizzoUpdate(IndirizzoBase):
    id: int


class IndirizzoDelete(BaseModel):
    id: int


class IndirizzoList(BaseModel):
    indirizzi: List[IndirizzoResponse]
    total: int
    offset: int
    limit: int
