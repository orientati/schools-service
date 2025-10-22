from __future__ import annotations

from pydantic import BaseModel


class CittaBase(BaseModel):  # indirizzo di studio
    nome: str
    provincia: str | None = None
    codice_postale: str | None = None


class CittaCreate(CittaBase):
    pass


class CittaUpdate(CittaBase):
    id: int


class CittaDelete(BaseModel):
    id: int


class CittaResponse(CittaBase):
    id: int | None = None
