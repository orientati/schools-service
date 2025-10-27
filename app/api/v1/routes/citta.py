from __future__ import annotations

from fastapi import APIRouter
from fastapi import Query

import app.services.citta as CittaService
from app.schemas.citta import CittaResponse, CittaList

router = APIRouter()


@router.get("/", response_model=CittaList)
async def get_citta(
        limit: int = Query(default=10, ge=1, le=100, description="Numero di città da restituire (1-100)"),
        offset: int = Query(default=0, ge=0, description="Numero di città da saltare per la paginazione"),
        search: str = Query(default=None, description="Termine di ricerca per filtrare le città per nome"),
        sort_by: str = Query(default=None, description="Campo per ordinamento (es. nome)"),
        order: str = Query(default="asc", regex="^(asc|desc)$", description="Ordine: asc o desc")
):
    """
    Recupera la lista delle città, con opzioni di paginazione e filtro.
    Args:
        limit (int): Numero di città da restituire (1-100)
        offset (int): Numero di città da saltare per la paginazione
        search (str): Termine di ricerca per filtrare le città per nome
        sort_by (str): Campo per ordinamento (es. nome)
        order (str): Ordine: asc o desc
    Returns:
        CittaList: Lista delle città con metadati di paginazione

    """
    try:
        return await CittaService.get_citta(
            limit=limit,
            offset=offset,
            search=search,
            sort_by=sort_by,
            order=order
        )
    except Exception as e:
        raise e


@router.get("/{citta_id}", response_model=CittaResponse)
async def get_citta_by_id(citta_id: int):
    """
    Recupera i dettagli di una città dato il suo ID.

    Args:
        citta_id (int): ID della città da recuperare

    Returns:
        CittaResponse: Dettagli della città
    """
    try:
        return await CittaService.get_citta_by_id(citta_id)
    except Exception as e:
        raise e


@router.post("/", response_model=CittaResponse)
async def post_citta(citta: CittaResponse):
    """
    Crea una nuova città.

    Args:
        citta (CittaResponse): Dati della città da creare

    Returns:
        CittaResponse: Dettagli della città creata
    """
    try:
        return await CittaService.post_citta(citta)
    except Exception as e:
        raise e


@router.put("/{citta_id}", response_model=CittaResponse)
async def put_citta(citta_id: int, citta: CittaResponse):
    """
    Aggiorna i dettagli di una città esistente.

    Args:
        citta_id (int): ID della città da aggiornare
        citta (CittaResponse): Dati aggiornati della città

    Returns:
        CittaResponse: Dettagli della città aggiornata
    """
    try:
        return await CittaService.put_citta(citta_id, citta)
    except Exception as e:
        raise e


@router.delete("/{citta_id}", response_model=dict)
async def delete_citta(citta_id: int):
    """
    Elimina una città dato il suo ID.

    Args:
        citta_id (int): ID della città da eliminare

    Returns:
        dict: Messaggio di conferma dell'eliminazione
    """
    try:
        return await CittaService.delete_citta(citta_id)
    except Exception as e:
        raise e
