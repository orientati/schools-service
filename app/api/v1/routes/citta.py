from __future__ import annotations
from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_db
import app.services.citta as CittaService
from app.schemas.citta import CittaList, CittaResponse, CittaCreate, CittaUpdate

router = APIRouter()

@router.get("/", response_model=CittaList)
async def get_citta(
        limit: int = Query(default=10, ge=1, le=100),
        offset: int = Query(default=0, ge=0),
        search: str = Query(default=None),
        sort_by: str = Query(default=None),
        order: str = Query(default="asc", regex="^(asc|desc)$"),
        db: AsyncSession = Depends(get_db)
):
    try:
        return await CittaService.get_citta(db, limit, offset, search, sort_by, order)
    except Exception as e:
        raise e

@router.get("/{citta_id}", response_model=CittaResponse)
async def get_citta_by_id(citta_id: int, db: AsyncSession = Depends(get_db)):
    try:
        return await CittaService.get_citta_by_id(citta_id, db)
    except Exception as e:
        raise e

@router.get("/zipcode/{zipcode}", response_model=CittaResponse)
async def get_citta_by_zipcode(zipcode: str, db: AsyncSession = Depends(get_db)):
    try:
        return await CittaService.get_citta_by_zipcode(zipcode, db)
    except Exception as e:
        raise e

@router.post("/", response_model=CittaResponse)
async def post_citta(citta: CittaCreate, db: AsyncSession = Depends(get_db)):
    try:
        return await CittaService.post_citta(citta, db)
    except Exception as e:
        raise e

@router.put("/{citta_id}", response_model=CittaResponse)
async def put_citta(citta_id: int, citta: CittaUpdate, db: AsyncSession = Depends(get_db)):
    try:
        return await CittaService.put_citta(citta_id, citta, db)
    except Exception as e:
        raise e

@router.delete("/{citta_id}")
async def delete_citta(citta_id: int, db: AsyncSession = Depends(get_db)):
    try:
        return await CittaService.delete_citta(citta_id, db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
