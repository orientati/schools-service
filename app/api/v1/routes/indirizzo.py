from __future__ import annotations

from fastapi import APIRouter

from app.schemas.indirizzo import IndirizzoList, IndirizzoResponse, IndirizzoCreate, IndirizzoUpdate, IndirizzoDelete

router = APIRouter()


@router.get("/", response_model=IndirizzoList)
async def get_indirizzi():  # TODO: aggiungere offset e limit
    """
    Recupera la lista degli indirizzi di studio disponibili.

    Returns:
        IndirizzoList: Lista degli indirizzi di studio
    """
    pass


@router.get("/{indirizzo_id}", response_model=IndirizzoResponse)
async def get_indirizzo_by_id(indirizzo_id: int):
    """
    Recupera i dettagli di un indirizzo di studio dato il suo ID.

    Args:
        indirizzo_id (int): ID dell'indirizzo di studio da recuperare

    Returns:
        IndirizzoResponse: Dettagli dell'indirizzo di studio
    """
    pass


@router.post("/", response_model=IndirizzoResponse)
async def post_indirizzo(indirizzo: IndirizzoCreate):
    """
    Crea un nuovo indirizzo di studio.

    Args:
        indirizzo (IndirizzoResponse): Dati dell'indirizzo di studio da creare

    Returns:
        IndirizzoResponse: Dettagli dell'indirizzo di studio creato
    """
    pass


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
    pass


@router.delete("/{indirizzo_id}")
async def delete_indirizzo(indirizzo: IndirizzoDelete):
    """
    Elimina un indirizzo di studio esistente.

    Args:
        indirizzo_id (int): ID dell'indirizzo di studio da eliminare
    """
    pass


@router.post("/link-school/{indirizzo_id}/{school_id}")
async def link_indirizzo_to_school(indirizzo_id: int, school_id: int
                                   ):
    """
    Collega un indirizzo di studio a una scuola.

    Args:
        indirizzo_id (int): ID dell'indirizzo di studio
        school_id (int): ID della scuola
    """
    pass
