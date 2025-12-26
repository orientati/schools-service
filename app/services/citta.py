from __future__ import annotations
from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Citta
from app.schemas.citta import CittaList, CittaResponse, CittaCreate, CittaUpdate

async def get_citta(
        db: AsyncSession,
        limit: int,
        offset: int,
        search: Optional[str],
        sort_by: Optional[str],
        order: Optional[str]
) -> CittaList:
    try:
        stmt = select(Citta)
        if search:
            stmt = stmt.filter(Citta.nome.ilike(f"%{search}%"))
        
        sort_column = {
            "name": Citta.nome,
        }.get(sort_by, Citta.nome)
        
        if order == "desc":
            stmt = stmt.order_by(sort_column.desc())
        else:
            stmt = stmt.order_by(sort_column)

        result = await db.execute(stmt.offset(offset).limit(limit))
        citta_list = result.scalars().all()
        
        # Proxy total count logic for compatibility with existing schema expectation
        return CittaList(
            total=len(citta_list), 
            limit=limit,
            offset=offset,
            citta=[CittaResponse(id=c.id, nome=c.nome, cap=c.codice_postale, provincia=c.provincia, regione=c.regione) for c in citta_list],
            filter_search=search,
            sort_by=sort_by,
            order=order
        )
    except Exception as e:
        raise e

async def get_citta_by_id(citta_id: int, db: AsyncSession) -> CittaResponse:
    try:
        stmt = select(Citta).filter(Citta.id == citta_id)
        result = await db.execute(stmt)
        citta = result.scalars().first()
        if not citta:
            raise Exception("Città non trovata")
        return CittaResponse(id=citta.id, nome=citta.nome, cap=citta.codice_postale, provincia=citta.provincia, regione=citta.regione)
    except Exception as e:
        raise e

async def get_citta_by_zipcode(cap: str, db: AsyncSession) -> CittaResponse:
    try:
        stmt = select(Citta).filter(Citta.codice_postale == cap)
        result = await db.execute(stmt)
        citta = result.scalars().first()
        if not citta:
            raise Exception("Città non trovata")
        return CittaResponse(id=citta.id, nome=citta.nome, cap=citta.codice_postale, provincia=citta.provincia, regione=citta.regione)
    except Exception as e:
        raise e

async def post_citta(citta: CittaCreate, db: AsyncSession) -> CittaResponse:
    try:
        stmt = select(Citta).filter(Citta.nome == citta.nome, Citta.codice_postale == citta.cap)
        result = await db.execute(stmt)
        existing_citta = result.scalars().first()
        if existing_citta:
            raise Exception("Città già esistente")
            
        new_citta = Citta(nome=citta.nome, codice_postale=citta.cap, provincia=citta.provincia, regione=citta.regione)
        db.add(new_citta)
        await db.commit()
        await db.refresh(new_citta)
        return CittaResponse(id=new_citta.id, nome=new_citta.nome, cap=new_citta.codice_postale, provincia=new_citta.provincia, regione=new_citta.regione)
    except Exception as e:
        raise e

async def put_citta(citta_id: int, citta: CittaUpdate, db: AsyncSession) -> CittaResponse:
    try:
        stmt = select(Citta).filter(Citta.id == citta_id)
        result = await db.execute(stmt)
        existing_citta = result.scalars().first()
        if not existing_citta:
            raise Exception("Città non trovata")

        existing_citta.nome = citta.nome
        existing_citta.codice_postale = citta.cap
        existing_citta.provincia = citta.provincia
        existing_citta.regione = citta.regione
        
        await db.commit()
        await db.refresh(existing_citta)
        return CittaResponse(id=existing_citta.id, nome=existing_citta.nome, cap=existing_citta.codice_postale, provincia=existing_citta.provincia, regione=existing_citta.regione)
    except Exception as e:
        raise e

async def delete_citta(citta_id: int, db: AsyncSession):
    try:
        stmt = select(Citta).filter(Citta.id == citta_id)
        result = await db.execute(stmt)
        citta = result.scalars().first()
        if not citta:
            raise Exception("Città non trovata")
        await db.delete(citta)
        await db.commit()
        return {"message": "Città eliminata con successo"}
    except Exception as e:
        raise e
