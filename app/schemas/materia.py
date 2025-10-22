from __future__ import annotations

from typing import List

from pydantic import BaseModel


class MateriaBase(BaseModel):
    nome: str
    descrizione: str | None = None


class MateriaResponse(MateriaBase):
    id: int | None = None


class MateriaCreate(MateriaBase):
    pass


class MateriaUpdate(MateriaBase):
    id: int


class MateriaDelete(BaseModel):
    id: int


class MateriaList(BaseModel):
    materie: List[MateriaResponse]
    total: int
    offset: int
    limit: int
