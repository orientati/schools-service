from __future__ import annotations
from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_db
from app.schemas.materia import MateriaResponse, MateriaList, MateriaUpdate, MateriaCreate
from app.services import materie as MaterieService

router = APIRouter()

@router.get("/", response_model=MateriaList)
async def get_materie(
        limit: int = Query(default=10, ge=1, le=100),
        offset: int = Query(default=0, ge=0),
        search: str = Query(default=None),
        sort_by: str = Query(default=None),
        order: str = Query(default="asc", regex="^(asc|desc)$"),
        db: AsyncSession = Depends(get_db)
):
    try:
        return await MaterieService.get_materie(db, limit, offset, search, sort_by, order)
    except Exception as e:
        raise e

@router.get("/{materia_id}", response_model=MateriaResponse)
async def get_materia_by_id(materia_id: int, db: AsyncSession = Depends(get_db)):
    try:
        return await MaterieService.get_materia_by_id(materia_id, db)
    except Exception as e:
        raise e

@router.post("/", response_model=MateriaResponse)
async def post_materia(materia: MateriaCreate, db: AsyncSession = Depends(get_db)):
    try:
        return await MaterieService.create_materia(materia, db)
    except Exception as e:
        raise e

@router.put("/{materia_id}", response_model=MateriaResponse)
async def put_materia(materia_id: int, materia: MateriaUpdate, db: AsyncSession = Depends(get_db)):
    try:
        return await MaterieService.update_materia(materia_id, materia, db)
    except Exception as e:
        raise e

@router.delete("/{materia_id}")
async def delete_materia(materia_id: int, db: AsyncSession = Depends(get_db)):
    try:
        return await MaterieService.delete_materia(materia_id, db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/link-indirizzo/{materia_id}/{indirizzo_id}")
async def link_materia_to_indirizzo(materia_id: int, indirizzo_id: int, db: AsyncSession = Depends(get_db)):
    try:
        return await MaterieService.link_materia_to_indirizzo(materia_id, indirizzo_id, db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/unlink-indirizzo/{materia_id}/{indirizzo_id}")
async def unlink_materia_from_indirizzo(materia_id: int, indirizzo_id: int, db: AsyncSession = Depends(get_db)):
    try:
        return await MaterieService.unlink_materia_from_indirizzo(materia_id, indirizzo_id, db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
