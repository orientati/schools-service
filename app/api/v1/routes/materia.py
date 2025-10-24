from __future__ import annotations

from fastapi import APIRouter
from fastapi import Query

from app.schemas.materia import MateriaResponse, MateriaList, MateriaCreate, MateriaUpdate
from app.services import materie as MaterieService

router = APIRouter()


@router.get("/", response_model=MateriaList)
async def get_materie(
        limit: int = Query(default=10, ge=1, le=100, description="Numero di materie da restituire (1-100)"),
        offset: int = Query(default=0, ge=0, description="Numero di materie da saltare per la paginazione"),
        search: str = Query(default=None, description="Termine di ricerca per filtrare le materie per nome"),
        order: str = Query(default="asc", regex="^(asc|desc)$", description="Ordine: asc o desc")
):
    """
    Recupera la lista delle materie, con opzioni di paginazione e filtro.


    Returns:
        MateriaList: Lista delle materie con metadati di paginazione
    """
    try:
        return await MaterieService.get_materie(
            limit=limit,
            offset=offset,
            search=search,
            order=order
        )
    except Exception as e:
        raise e


@router.get("/{materia_id}", response_model=MateriaResponse)
async def get_materia_by_id(materia_id: int):
    """
    Recupera i dettagli di una materia dato il suo ID.

    Args:
        materia_id (int): ID della materia da recuperare

    Returns:
        MateriaResponse: Dettagli della materia
    """
    try:
        return await MaterieService.get_materia_by_id(materia_id)
    except Exception as e:
        raise e


@router.post("/", response_model=MateriaResponse)
async def post_materia(materia: MateriaCreate):
    """
    Crea una nuova materia.

    Args:
        materia (MateriaResponse): Dati della materia da creare

    Returns:
        MateriaResponse: Dettagli della materia creata
    """
    pass


@router.put("/{materia_id}", response_model=MateriaResponse)
async def put_materia(materia_id: int, materia: MateriaUpdate):
    """
    Aggiorna i dettagli di una materia esistente.

    Args:
        materia_id (int): ID della materia da aggiornare
        materia (MateriaResponse): Dati aggiornati della materia

    Returns:
        MateriaResponse: Dettagli della materia aggiornata
    """
    pass


@router.delete("/{materia_id}", response_model=MateriaResponse)
async def delete_materia(materia_id: int):
    """
    Elimina una materia esistente.

    Args:
        materia_id (int): ID della materia da eliminare

    Returns:
        MateriaResponse: Dettagli della materia eliminata
    """
    pass


@router.post("/link-indirizzo/{materia_id}/{indirizzo_id}")
async def link_materia_to_indirizzo(materia_id: int, indirizzo_id:
int):
    """
    Collega una materia a un indirizzo di studio.

    Args:
        materia_id (int): ID della materia da collegare
        indirizzo_id (int): ID dell'indirizzo di studio a cui collegare la materia
    """
    pass
