from __future__ import annotations

from app.api.deps import get_db
from app.models import Materia, Indirizzo
from app.schemas.materia import MateriaList, MateriaResponse, MateriaUpdate


def build_materia(materie) -> MateriaResponse:
    return MateriaResponse(
        id=materie.id,
        nome=materie.nome,
        descrizione=materie.descrizione
    )


async def get_materie(
        limit: int = 100,
        offset: int = 0,
        search: str | None = None,
        sort_by: str | None = None,
        order: str | None = None
) -> MateriaList:
    """Recupera la lista delle materie con opzioni di paginazione e filtro.

    Args:
        limit (int): Numero massimo di materie da restituire.
        offset (int): Numero di materie da saltare per la paginazione.
        search (str | None): Termine di ricerca per filtrare le materie per nome.
        sort_by (str | None): Campo per ordinamento (es. nome).
        order (str | None): Ordine: 'asc' o 'desc'.

    Returns:
        MateriaList: Lista delle materie con metadati di paginazione.
    """
    try:
        db = next(get_db())
        query = db.query(Materia)
        # applico i filtri
        if search:
            query = query.filter(Materia.nome.ilike(f"%{search}%"))
        # applico l'ordinamento
        sort_column = {
            "name": Materia.nome,
        }.get(sort_by, Materia.nome)
        if order == "desc":
            sort_column = sort_column.desc()
        query = query.order_by(sort_column)
        total = query.count()
        materie = query.offset(offset).limit(limit).all()
        return MateriaList(
            total=total,
            limit=limit,
            offset=offset,
            materie=[build_materia(m) for m in materie],
            filter_search=search,
            sort_by=sort_by,
            order=order
        )
    except Exception as e:
        raise e


async def get_materia_by_id(materia_id: int) -> MateriaResponse:
    """Recupera i dettagli di una materia dato il suo ID.

    Args:
        materia_id (int): ID della materia da recuperare.

    Returns:
        MateriaResponse: Dettagli della materia.
    """
    try:
        db = next(get_db())
        materia = db.query(Materia).filter(Materia.id == materia_id).first()
        if not materia:
            raise Exception(f"Materia con ID {materia_id} non trovata.")
        return build_materia(materia)
    except Exception as e:
        raise e


async def create_materia(materia_data: MateriaResponse) -> MateriaResponse:
    """Crea una nuova materia.

    Args:
        materia_data (MateriaResponse): Dati della materia da creare.

    Returns:
        MateriaResponse: Dettagli della materia creata.
    """
    try:
        db = next(get_db())
        nuova_materia = Materia(
            nome=materia_data.nome,
            descrizione=materia_data.descrizione
        )
        db.add(nuova_materia)
        db.commit()
        db.refresh(nuova_materia)
        return build_materia(nuova_materia)
    except Exception as e:
        raise e


async def update_materia(materia_id: int, materia_data: MateriaUpdate) -> MateriaResponse:
    """Aggiorna i dettagli di una materia esistente.

    Args:
        materia_id (int): ID della materia da aggiornare.
        materia_data (MateriaUpdate): Dati aggiornati della materia.

    Returns:
        MateriaResponse: Dettagli della materia aggiornata.
    """
    try:
        db = next(get_db())
        materia = db.query(Materia).filter(Materia.id == materia_id).first()
        if not materia:
            raise Exception(f"Materia con ID {materia_id} non trovata.")
        materia.nome = materia_data.nome
        materia.descrizione = materia_data.descrizione
        db.commit()
        db.refresh(materia)
        return build_materia(materia)
    except Exception as e:
        raise e


async def delete_materia(materia_id):
    try:
        db = next(get_db())
        materia = db.query(Materia).filter(Materia.id == materia_id).first()
        if not materia:
            raise Exception(f"Materia con ID {materia_id} non trovata.")
        if materia.indirizzi:
            raise Exception(
                f"Impossibile eliminare la materia con ID {materia_id} perché collegata a uno o più indirizzi di studio.")
        db.delete(materia)
        db.commit()
        return {"message": f"Materia {materia_id} eliminata con successo."}
    except Exception as e:
        raise e


async def link_materia_to_indirizzo(materia_id, indirizzo_id):
    try:
        db = next(get_db())
        materia = db.query(Materia).filter(Materia.id == materia_id).first()
        if not materia:
            raise Exception(f"Materia con ID {materia_id} non trovata.")
        indirizzo = db.query(Indirizzo).filter(Indirizzo.id == indirizzo_id).first()
        if not indirizzo:
            raise Exception(f"Indirizzo con ID {indirizzo_id} non trovato.")
        if indirizzo in materia.indirizzi:
            raise Exception(f"Indirizzo con ID {indirizzo_id} già collegato alla materia con ID {materia_id}.")
        materia.indirizzi.append(indirizzo)
        db.commit()
        db.refresh(materia)
        return build_materia(materia)
    except Exception as e:
        raise e


async def unlink_materia_from_indirizzo(materia_id, indirizzo_id):
    try:
        db = next(get_db())
        materia = db.query(Materia).filter(Materia.id == materia_id).first()
        if not materia:
            raise Exception(f"Materia con ID {materia_id} non trovata.")
        indirizzo = db.query(Indirizzo).filter(Indirizzo.id == indirizzo_id).first()
        if not indirizzo:
            raise Exception(f"Indirizzo con ID {indirizzo_id} non trovato.")
        if indirizzo not in materia.indirizzi:
            raise Exception(f"Indirizzo con ID {indirizzo_id} non collegato alla materia con ID {materia_id}.")
        materia.indirizzi.remove(indirizzo)
        db.commit()
        db.refresh(materia)
        return build_materia(materia)
    except Exception as e:
        raise e
