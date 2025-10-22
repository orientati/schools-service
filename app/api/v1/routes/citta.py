from __future__ import annotations

from fastapi import APIRouter

from app.schemas.citta import CittaResponse

router = APIRouter()


@router.get("/", response_model=CittaResponse)
async def get_citta():
    """
    Recupera la lista delle città disponibili.

    Returns:
        CittaResponse: Lista delle città
    """
    pass


@router.get("/{citta_id}", response_model=CittaResponse)
async def get_citta_by_id(citta_id: int):
    """
    Recupera i dettagli di una città dato il suo ID.

    Args:
        citta_id (int): ID della città da recuperare

    Returns:
        CittaResponse: Dettagli della città
    """
    pass


@router.post("/", response_model=CittaResponse)
async def post_citta(citta: CittaResponse):
    """
    Crea una nuova città.

    Args:
        citta (CittaResponse): Dati della città da creare

    Returns:
        CittaResponse: Dettagli della città creata
    """
    pass


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
    pass


@router.delete("/{citta_id}", response_model=dict)
async def delete_citta(citta_id: int):
    """
    Elimina una città dato il suo ID.

    Args:
        citta_id (int): ID della città da eliminare

    Returns:
        dict: Messaggio di conferma dell'eliminazione
    """
    pass
