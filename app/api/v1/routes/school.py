from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends
from fastapi import Query
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.schemas.school import SchoolsList, SchoolResponse, SchoolCreate, SchoolDeleteResponse, SchoolUpdate
from app.services import school as school_service
from app.services.http_client import OrientatiException

router = APIRouter()


@router.get("/", response_model=SchoolsList)
async def get_schools(
        limit: int = Query(default=10, ge=1, le=100, description="Numero di scuole da restituire (1-100)"),
        offset: int = Query(default=0, ge=0, description="Numero di scuole da saltare per la paginazione"),
        search: Optional[str] = Query(default=None, description="Termine di ricerca per filtrare le scuole per nome"),
        tipo: Optional[str] = Query(default=None, description="Filtra per tipo di scuola (es. Liceo, ITIS, ecc.)"),
        citta: Optional[str] = Query(default=None, description="Filtra per città"),
        provincia: Optional[str] = Query(default=None, description="Filtra per provincia"),
        indirizzo: Optional[str] = Query(default=None,
                                         description="Filtra per tipo di scuola (es. Liceo, informatico, ecc.)"),
        sort_by: str = Query(default="name", description="Campo per ordinamento (es. nome, città, provincia)"),
        order: str = Query(default="asc", regex="^(asc|desc)$", description="Ordine: asc o desc"),
        db: AsyncSession = Depends(get_db)
):
    """
    Recupera la lista delle scuole con opzioni di paginazione e filtro.

    Returns:
        dict: Lista delle scuole con metadati di paginazione
    """
    try:
        return await school_service.get_schools(
            db=db,
            limit=limit,
            offset=offset,
            search=search,
            tipo=tipo,
            citta=citta,
            provincia=provincia,
            indirizzo=indirizzo,
            sort_by=sort_by,
            order=order
        )
    except OrientatiException as e:
        return JSONResponse(
            status_code=e.status_code,
            content={
                "message": e.message,
                "details": e.details,
                "url": e.url
            }
        )


@router.get("/{school_id}", response_model=SchoolResponse)
async def get_school_by_id(school_id: int, db: AsyncSession = Depends(get_db)) -> SchoolResponse:
    """
    Recupera i dettagli di una scuola dato il suo ID.

    Args:
        school_id (int): ID della scuola da recuperare.

    Returns:
        SchoolResponse: Dettagli della scuola.
    """
    try:
        return await school_service.get_school_by_id(school_id, db)
    except OrientatiException as e:
        return JSONResponse(
            status_code=e.status_code,
            content={
                "message": e.message,
                "details": e.details,
                "url": e.url
            }
        )


@router.post("/", response_model=SchoolResponse)
async def post_school(school: SchoolCreate, db: AsyncSession = Depends(get_db)) -> SchoolResponse:
    """
    Crea una nuova scuola.
    Args:
        school (SchoolCreate): Dati della scuola da creare.
    Returns:
        SchoolResponse: Dettagli della scuola creata.
    """
    try:
        scuola = await school_service.create_school(school, db)
        print(scuola)
        return scuola
    except OrientatiException as e:
        return JSONResponse(
            status_code=e.status_code,
            content={
                "message": e.message,
                "details": e.details,
                "url": e.url
            }
        )


@router.put("/{school_id}", response_model=SchoolResponse)
async def put_school(school_id: int, school: SchoolUpdate, db: AsyncSession = Depends(get_db)) -> SchoolResponse:
    """
    Aggiorna i dettagli di una scuola esistente.
    Args:
        school_id (int): ID della scuola da aggiornare.
        school (SchoolUpdate): Dati aggiornati della scuola.
    Returns:
        SchoolResponse: Dettagli della scuola aggiornata.
    """
    try:
        return await school_service.update_school(school_id, school.model_dump(), db)
    except OrientatiException as e:
        return JSONResponse(
            status_code=e.status_code,
            content={
                "message": e.message,
                "details": e.details,
                "url": e.url
            }
        )


@router.delete("/{school_id}", response_model=SchoolDeleteResponse)
async def delete_school(school_id: int, db: AsyncSession = Depends(get_db)) -> SchoolDeleteResponse:
    """
    Elimina una scuola esistente.
    Args:
        school_id (int): ID della scuola da eliminare.
    Returns:
        SchoolDeleteResponse: Conferma dell'eliminazione della scuola.
    """
    try:
        return await school_service.delete_school(school_id, db)
    except OrientatiException as e:
        return JSONResponse(
            status_code=e.status_code,
            content={
                "message": e.message,
                "details": e.details,
                "url": e.url
            }
        )
