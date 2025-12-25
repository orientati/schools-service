from pydantic import BaseModel
from typing import Optional, List

class MateriaBase(BaseModel):
    nome: str
    descrizione: str

class MateriaCreate(MateriaBase):
    pass

class MateriaUpdate(MateriaBase):
    pass

class MateriaResponse(MateriaBase):
    id: int
    class Config:
        from_attributes = True

class MateriaList(BaseModel):
    total: int
    limit: int
    offset: int
    materie: List[MateriaResponse]
    filter_search: Optional[str] = None
    sort_by: Optional[str] = None
    order: Optional[str] = None
