from pydantic import BaseModel
from typing import Optional, List

class CittaBase(BaseModel):
    nome: str
    cap: str
    provincia: str
    regione: str

class CittaCreate(CittaBase):
    pass

class CittaUpdate(CittaBase):
    pass

class CittaResponse(CittaBase):
    id: int
    class Config:
        from_attributes = True

class CittaList(BaseModel):
    total: int
    limit: int
    offset: int
    citta: List[CittaResponse]
    filter_search: Optional[str] = None
    sort_by: Optional[str] = None
    order: Optional[str] = None
