from __future__ import annotations

from fastapi import APIRouter

from app.schemas.materia import MateriaResponse, MateriaList, MateriaCreate, MateriaUpdate

router = APIRouter()


@router.get("/", response_model=MateriaList)
async def get_materie():  # TODO: aggiungere offset e limit
    """
    Recupera la lista delle materie disponibili.

    Returns:
        MateriaList: Lista delle materie
    """
    pass


@router.get("/{materia_id}", response_model=MateriaResponse)
async def get_materia_by_id(materia_id: int):
    """
    Recupera i dettagli di una materia dato il suo ID.

    Args:
        materia_id (int): ID della materia da recuperare

    Returns:
        MateriaResponse: Dettagli della materia
    """
    pass


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
