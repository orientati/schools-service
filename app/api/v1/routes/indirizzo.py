from __future__ import annotations
from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_db
import app.services.indirizzi as IndirizziService
from app.schemas.indirizzo import IndirizzoList, IndirizzoResponse, IndirizzoCreate, IndirizzoUpdate

router = APIRouter()

@router.get("/", response_model=IndirizzoList)
async def get_indirizzi(
        limit: int = Query(default=10, ge=1, le=100),
        offset: int = Query(default=0, ge=0),
        search: str = Query(default=None),
        sort_by: str = Query(default=None),
        order: str = Query(default="asc", pattern="^(asc|desc)$"),
        db: AsyncSession = Depends(get_db)
):
    try:
        return await IndirizziService.get_indirizzi(db, limit, offset, search, sort_by, order)
    except Exception as e:
        raise e

@router.get("/{indirizzo_id}", response_model=IndirizzoResponse)
async def get_indirizzo_by_id(indirizzo_id: int, db: AsyncSession = Depends(get_db)):
    try:
        return await IndirizziService.get_indirizzo_by_id(indirizzo_id, db)
    except Exception as e:
        raise e

@router.post("/", response_model=IndirizzoResponse)
async def post_indirizzo(indirizzo: IndirizzoCreate, db: AsyncSession = Depends(get_db)):
    try:
        return await IndirizziService.post_indirizzo(indirizzo, db)
    except Exception as e:
        raise e

@router.put("/{indirizzo_id}", response_model=IndirizzoResponse)
async def put_indirizzo(indirizzo_id: int, indirizzo: IndirizzoUpdate, db: AsyncSession = Depends(get_db)):
    try:
        return await IndirizziService.put_indirizzo(indirizzo_id, indirizzo, db)
    except Exception as e:
        raise e

@router.delete("/{indirizzo_id}")
async def delete_indirizzo(indirizzo_id: int, db: AsyncSession = Depends(get_db)):
    try:
        return await IndirizziService.delete_indirizzo(indirizzo_id, db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
