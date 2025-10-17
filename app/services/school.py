from __future__ import annotations

from typing import Optional

from app.api.deps import get_db
from app.models import Scuola
from app.schemas.school import SchoolsList, SchoolBase


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
    # applico i filtri
    if search:
        query = query.filter(Scuola.nome.ilike(f"%{search}%"))
    if tipo:
        query = query.filter(Scuola.tipo == tipo)
    if citta:
        query = query.join(Scuola.citta).filter_by(nome=citta)
    if provincia:
        query = query.join(Scuola.citta).filter_by(provincia=provincia)
    if indirizzo:
        query = query.filter(Scuola.indirizzo.ilike(f"%{indirizzo}%"))
    # applico l'ordinamento
    sort_column = {
        "name": Scuola.nome,
        "citta": Scuola.citta.has(),
        "provincia": Scuola.citta.has()
    }.get(sort_by, Scuola.nome)
    if order == "desc":
        sort_column = sort_column.desc()
    query = query.order_by(sort_column)
    total = query.count()
    scuole = query.offset(offset).limit(limit).all()
    return SchoolsList(
        total=total,
        limit=limit,
        offset=offset,
        scuole=SchoolBase(
            nome=scuola.nome,
            tipo=scuola.tipo,
            indirizzo=scuola.indirizzo,
            città=scuola.citta.nome,
            provincia=scuola.citta.provincia,
            codice_postale=scuola.citta.codice_postale,
            email_contatto=scuola.email_contatto,
            telefono_contatto=scuola.telefono_contatto,
            indirizzi_scuola=[],  # da implementare
            sito_web=scuola.sito_web,
            descrizione=scuola.descrizione,
            created_at=scuola.created_at,
            updated_at=scuola.updated_at
        )
    for scuola in scuole,
    filter_search=search,
    filter_tipo=tipo,
    filter_citta=citta,
    filter_provincia=provincia,
    filter_indirizzo=indirizzo,
    sort_by=sort_by,
    order=order
    )
