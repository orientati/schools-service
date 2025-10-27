from __future__ import annotations

from fastapi import APIRouter, HTTPException
from fastapi import Query

import app.services.indirizzi as IndirizziService
from app.schemas.indirizzo import IndirizzoList, IndirizzoResponse, IndirizzoCreate, IndirizzoUpdate

router = APIRouter()


@router.get("/", response_model=IndirizzoList)
async def get_indirizzi(
        limit: int = Query(default=10, ge=1, le=100, description="Numero di indirizzi da restituire (1-100)"),
        offset: int = Query(default=0, ge=0, description="Numero di indirizzi da saltare per la paginazione"),
        search: str = Query(default=None, description="Termine di ricerca per filtrare gli indirizzi per nome"),
        sort_by: str = Query(default=None, description="Campo per ordinamento (es. nome)"),
        order: str = Query(default="asc", regex="^(asc|desc)$", description="Ordine: asc o desc")
):
    """
    Recupera la lista degli indirizzi di studio disponibili.

    Returns:
        IndirizzoList: Lista degli indirizzi di studio
    """

    try:
        return await IndirizziService.get_indirizzi(
            limit=limit,
            offset=offset,
            search=search,
            sort_by=sort_by,
            order=order
        )
    except Exception as e:
        raise e


@router.get("/{indirizzo_id}", response_model=IndirizzoResponse)
async def get_indirizzo_by_id(indirizzo_id: int):
    """
    Recupera i dettagli di un indirizzo di studio dato il suo ID.

    Args:
        indirizzo_id (int): ID dell'indirizzo di studio da recuperare

    Returns:
        IndirizzoResponse: Dettagli dell'indirizzo di studio
    """
    try:
        return await IndirizziService.get_indirizzo_by_id(indirizzo_id)
    except Exception as e:
        raise e


@router.post("/", response_model=IndirizzoResponse)
async def post_indirizzo(indirizzo: IndirizzoCreate):
    """
    Crea un nuovo indirizzo di studio.

    Args:
        indirizzo (IndirizzoCreate): Dati dell'indirizzo di studio da creare

    Returns:
        IndirizzoResponse: Dettagli dell'indirizzo di studio creato
    """
    try:
        return await IndirizziService.post_indirizzo(indirizzo)
    except Exception as e:
        raise e


@router.put("/{indirizzo_id}", response_model=IndirizzoResponse)
async def put_indirizzo(indirizzo_id: int, indirizzo: IndirizzoUpdate):
    """
    Aggiorna i dettagli di un indirizzo di studio esistente.

    Args:
        indirizzo_id (int): ID dell'indirizzo di studio da aggiornare
        indirizzo (IndirizzoResponse): Dati aggiornati dell'indirizzo di studio

    Returns:
        IndirizzoResponse: Dettagli dell'indirizzo di studio aggiornato
    """
    try:
        return await IndirizziService.put_indirizzo(indirizzo_id, indirizzo)
    except Exception as e:
        raise e


@router.delete("/{indirizzo_id}")
async def delete_indirizzo(indirizzo_id: int):
    """
    Elimina un indirizzo di studio esistente.

    Args:
        indirizzo_id (int): ID dell'indirizzo di studio da eliminare
    """
    try:
        return await IndirizziService.delete_indirizzo(indirizzo_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))  # TODO: da modificare
