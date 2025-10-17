from __future__ import annotations

from typing import Optional

from app.api.deps import get_db
from app.models import Scuola
from app.schemas.school import SchoolsList


async def get_schools(
        limit: int = 10,
        offset: int = 0,
        search: Optional[str] = None,
        tipo: Optional[str] = None,
        citta: Optional[str] = None,
        provincia: Optional[str] = None,
        indirizzo: Optional[str] = None,
        sort_by: str = "name",
        order: str = "asc"
) -> SchoolsList:
    """
    Recupera la lista delle scuole con opzioni di paginazione e filtro.

    Args:
        limit (int): Numero massimo di scuole da restituire.
        offset (int): Numero di scuole da saltare per la paginazione.
        search (Optional[str]): Termine di ricerca per filtrare le scuole per nome.
        tipo (Optional[str]): Filtra per tipo di scuola (es. Liceo, ITIS, ecc.).
        citta (Optional[str]): Filtra per città.
        provincia (Optional[str]): Filtra per provincia.
        indirizzo (Optional[str]): Filtra per tipo di studi (es. liceo classico, informatico, ecc.).
        sort_by (str): Campo per ordinamento (es. nome, città, provincia).
        order (str): Ordine: 'asc' o 'desc'.

    Returns:
        SchoolsList: Lista delle scuole con metadati di paginazione.
    """
    db = next(get_db())
    query = db.query(Scuola)
