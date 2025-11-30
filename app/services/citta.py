from __future__ import annotations

from app.api.deps import get_db
from app.models import Citta
from app.schemas.citta import CittaList, CittaResponse, CittaCreate, CittaUpdate


def build_citta(citta: Citta) -> CittaResponse:
    return CittaResponse(
        id=citta.id,
        nome=citta.nome,
        provincia=citta.provincia,
        codice_postale=citta.codice_postale
    )


async def get_citta(limit, offset, search, sort_by, order) -> CittaList:
    """
    Recupera la lista delle città con opzioni di paginazione e filtro.
    Args:
        limit (int): Numero massimo di città da restituire.
        offset (int): Numero di città da saltare per la paginazione.
        search (str | None): Termine di ricerca per filtrare le città per nome.
        sort_by (str | None): Campo per ordinamento (es. nome).
        order (str | None): Ordine: 'asc' o 'desc'.
    Returns:
        CittaList: Lista delle città con metadati di paginazione.
    """
    try:
        db = next(get_db())
        query = db.query(Citta)
        # applico i filtri
        if search:
            query = query.filter(Citta.nome.ilike(f"%{search}%"))
        # applico l'ordinamento
        sort_column = {
            "name": Citta.nome,
        }.get(sort_by, Citta.nome)
        if order == "desc":
            sort_column = sort_column.desc()
        query = query.order_by(sort_column)
        total = query.count()
        citta = query.offset(offset).limit(limit).all()
        return CittaList(
            total=total,
            limit=limit,
            offset=offset,
            citta=[build_citta(c) for c in citta],
            filter_search=search,
            sort_by=sort_by,
            order=order
        )
    except Exception as e:
        raise e


async def get_citta_by_id(citta_id: int) -> CittaResponse:
    """
    Recupera i dettagli di una città dato il suo ID.

    Args:
        citta_id (int): ID della città da recuperare

    Returns:
        Citta: Dettagli della città
    """
    try:
        db = next(get_db())
        citta = db.query(Citta).filter(Citta.id == citta_id).first()
        if not citta:
            raise Exception("Città non trovata")
        return build_citta(citta)
    except Exception as e:
        raise e


async def post_citta(citta: CittaCreate) -> CittaResponse:
    """
    Crea una nuova città.

    Args:
        citta (CittaCreate): Dati della città da creare

    Returns:
        CittaResponse: Dettagli della città creata
    """
    try:
        db = next(get_db())
        nuova_citta = Citta(
            nome=citta.nome,
            provincia=citta.provincia,
            codice_postale=citta.codice_postale
        )
        db.add(nuova_citta)
        db.commit()
        db.refresh(nuova_citta)
        return build_citta(nuova_citta)
    except Exception as e:
        raise e


async def put_citta(citta_id: int, citta: CittaUpdate) -> CittaResponse:
    """
    Aggiorna i dettagli di una città esistente.

    Args:
        citta_id (int): ID della città da aggiornare
        citta (CittaUpdate): Dati aggiornati della città

    Returns:
        CittaResponse: Dettagli della città aggiornata
    """
    try:
        db = next(get_db())
        citta_db = db.query(Citta).filter(Citta.id == citta_id).first()
        if not citta_db:
            raise Exception("Città non trovata")
        if citta.nome is not None:
            citta_db.nome = citta.nome
        if citta.provincia is not None:
            citta_db.provincia = citta.provincia
        if citta.codice_postale is not None:
            citta_db.codice_postale = citta.codice_postale
        db.commit()
        db.refresh(citta_db)
        return build_citta(citta_db)
    except Exception as e:
        raise e


async def delete_citta(citta_id: int) -> dict:
    """
    Elimina una città esistente.

    Args:
        citta_id (int): ID della città da eliminare

    Returns:
        dict: Messaggio di conferma dell'eliminazione
    """
    try:
        db = next(get_db())
        citta_db = db.query(Citta).filter(Citta.id == citta_id).first()
        if not citta_db:
            raise Exception("Città non trovata")
        db.delete(citta_db)
        db.commit()
        return {"message": "Città eliminata con successo"}
    except Exception as e:
        raise e


async def get_citta_by_zipcode(zipcode: str) -> CittaResponse:
    """
    Recupera i dettagli di una città dato il suo CAP.
    Args:
        zipcode (str): CAP della città da recuperare
    Returns:
        CittaResponse: Dettagli della città
    """
    try:
        db = next(get_db())
        citta = db.query(Citta).filter(Citta.codice_postale == zipcode).first()
        if not citta:
            raise Exception("Città non trovata")
        return build_citta(citta)
    except Exception as e:
        raise e
