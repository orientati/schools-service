from pydantic import BaseModel
from typing import Optional, List

class IndirizzoBase(BaseModel):
    nome: str
    descrizione: str
    id_scuola: int

class IndirizzoCreate(IndirizzoBase):
    pass

class IndirizzoUpdate(IndirizzoBase):
    pass

class IndirizzoResponse(IndirizzoBase):
    id: int
    class Config:
        from_attributes = True

class IndirizzoList(BaseModel):
    total: int
    limit: int
    offset: int
    indirizzi: List[IndirizzoResponse]
    filter_search: Optional[str] = None
    sort_by: Optional[str] = None
    order: Optional[str] = None
