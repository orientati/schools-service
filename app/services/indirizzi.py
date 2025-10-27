from __future__ import annotations

from app.api.deps import get_db
from app.models import Indirizzo
from app.schemas.indirizzo import IndirizzoList, IndirizzoResponse, IndirizzoCreate, IndirizzoUpdate


def build_indirizzo(indirizzo: Indirizzo) -> IndirizzoResponse:
    return IndirizzoResponse(
        id=indirizzo.id,
        nome=indirizzo.nome,
        descrizione=indirizzo.descrizione,
        id_scuola=indirizzo.id_scuola
    )


async def get_indirizzi(
        limit: int = 100,
        offset: int = 0,
        search: str | None = None,
        sort_by: str | None = None,
        order: str | None = None) -> IndirizzoList:
    """
    Recupera la lista degli indirizzi di studio disponibili.
    Args:
        limit (int): Numero massimo di indirizzi da restituire.
        offset (int): Numero di indirizzi da saltare per la paginazione.
        search (str | None): Termine di ricerca per filtrare gli indirizzi per nome.
        sort_by (str | None): Campo per ordinamento (es. nome).
        order (str | None): Ordine: 'asc' o 'desc'.
    Returns:
        IndirizzoList: Lista degli indirizzi di studio con metadati di paginazione.
    """
    try:
        db = next(get_db())
        query = db.query(Indirizzo)
        # applico i filtri
        if search:
            query = query.filter(Indirizzo.nome.ilike(f"%{search}%"))
        # applico l'ordinamento
        sort_column = {
            "name": Indirizzo.nome,
        }.get(sort_by, Indirizzo.nome)
        if order == "desc":
            sort_column = sort_column.desc()
        query = query.order_by(sort_column)
        total = query.count()
        indirizzi = query.offset(offset).limit(limit).all()
        return IndirizzoList(
            total=total,
            limit=limit,
            offset=offset,
            indirizzi=[build_indirizzo(i) for i in indirizzi],
            filter_search=search,
            sort_by=sort_by,
            order=order
        )
    except Exception as e:
        raise e


async def get_indirizzo_by_id(indirizzo_id: int) -> IndirizzoResponse:
    """
    Recupera i dettagli di un indirizzo di studio dato il suo ID.

    Args:
        indirizzo_id (int): ID dell'indirizzo di studio da recuperare

    Returns:
        IndirizzoResponse: Dettagli dell'indirizzo di studio
    """
    try:
        db = next(get_db())
        indirizzo = db.query(Indirizzo).filter(Indirizzo.id == indirizzo_id).first()
        if not indirizzo:
            raise Exception("Indirizzo non trovato")
        return build_indirizzo(indirizzo)
    except Exception as e:
        raise e


async def post_indirizzo(indirizzo: IndirizzoCreate) -> IndirizzoResponse:
    """
    Crea un nuovo indirizzo di studio.

    Args:
        indirizzo (IndirizzoCreate): Dati dell'indirizzo di studio da creare

    Returns:
        IndirizzoResponse: Dettagli dell'indirizzo di studio creato
    """
    try:
        db = next(get_db())
        new_indirizzo = Indirizzo(
            nome=indirizzo.nome,
            descrizione=indirizzo.descrizione,
            id_scuola=indirizzo.id_scuola
        )
        db.add(new_indirizzo)
        db.commit()
        db.refresh(new_indirizzo)
        return build_indirizzo(new_indirizzo)
    except Exception as e:
        raise e


async def put_indirizzo(indirizzo_id: int, indirizzo: IndirizzoUpdate) -> IndirizzoResponse:
    """
    Aggiorna i dettagli di un indirizzo di studio esistente.

    Args:
        indirizzo_id (int): ID dell'indirizzo di studio da aggiornare
        indirizzo (IndirizzoUpdate): Dati aggiornati dell'indirizzo di studio

    Returns:
        IndirizzoResponse: Dettagli dell'indirizzo di studio aggiornato
    """
    try:
        db = next(get_db())
        existing_indirizzo = db.query(Indirizzo).filter(Indirizzo.id == indirizzo_id).first()
        if not existing_indirizzo:
            raise Exception("Indirizzo non trovato")
        existing_indirizzo.nome = indirizzo.nome
        existing_indirizzo.descrizione = indirizzo.descrizione
        db.commit()
        db.refresh(existing_indirizzo)
        return build_indirizzo(existing_indirizzo)
    except Exception as e:
        raise e


async def delete_indirizzo(indirizzo_id: int):
    """
    Elimina un indirizzo di studio esistente.

    Args:
        indirizzo_id (int): ID dell'indirizzo di studio da eliminare
    """
    try:
        db = next(get_db())
        indirizzo = db.query(Indirizzo).filter(Indirizzo.id == indirizzo_id).first()
        if not indirizzo:
            raise Exception("Indirizzo non trovato")
        db.delete(indirizzo)
        db.commit()
        return {"message": "Indirizzo eliminato con successo"}
    except Exception as e:
        raise e