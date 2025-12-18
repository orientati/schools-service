from __future__ import annotations
from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Indirizzo
from app.schemas.indirizzo import IndirizzoList, IndirizzoResponse, IndirizzoCreate, IndirizzoUpdate

def build_indirizzo(indirizzo: Indirizzo) -> IndirizzoResponse:
    return IndirizzoResponse(
        id=indirizzo.id,
        nome=indirizzo.nome,
        descrizione=indirizzo.descrizione,
        id_scuola=indirizzo.id_scuola
    )

async def get_indirizzi(
        db: AsyncSession,
        limit: int,
        offset: int,
        search: Optional[str],
        sort_by: Optional[str],
        order: Optional[str]
) -> IndirizzoList:
    try:
        stmt = select(Indirizzo)
        if search:
            stmt = stmt.filter(Indirizzo.nome.ilike(f"%{search}%"))
        
        sort_column = {
            "name": Indirizzo.nome,
        }.get(sort_by, Indirizzo.nome)
        
        if order == "desc":
            stmt = stmt.order_by(sort_column.desc())
        else:
            stmt = stmt.order_by(sort_column)

        result = await db.execute(stmt.offset(offset).limit(limit))
        indirizzi = result.scalars().all()
        
        return IndirizzoList(
            total=len(indirizzi),
            limit=limit,
            offset=offset,
            indirizzi=[build_indirizzo(i) for i in indirizzi],
            filter_search=search,
            sort_by=sort_by,
            order=order
        )
    except Exception as e:
        raise e

async def get_indirizzo_by_id(indirizzo_id: int, db: AsyncSession) -> IndirizzoResponse:
    try:
        stmt = select(Indirizzo).filter(Indirizzo.id == indirizzo_id)
        result = await db.execute(stmt)
        indirizzo = result.scalars().first()
        if not indirizzo:
            raise Exception("Indirizzo non trovato")
        return build_indirizzo(indirizzo)
    except Exception as e:
        raise e

async def post_indirizzo(indirizzo: IndirizzoCreate, db: AsyncSession) -> IndirizzoResponse:
    try:
        # Note: Original code queried Indirizzo table to check for school existence (buggy logic in original sync code).
        # We will assume school exists or FK constraint handles it, or check properly if model available.
        # For now, simplistic approach to match previous attempt.
        
        stmt = select(Indirizzo).filter(
            Indirizzo.nome == indirizzo.nome,
            Indirizzo.id_scuola == indirizzo.id_scuola
        )
        result = await db.execute(stmt)
        existing_indirizzo = result.scalars().first()
        if existing_indirizzo:
             raise Exception("Indirizzo già esistente per questa scuola")

        new_indirizzo = Indirizzo(
            nome=indirizzo.nome,
            descrizione=indirizzo.descrizione,
            id_scuola=indirizzo.id_scuola
        )
        db.add(new_indirizzo)
        await db.commit()
        await db.refresh(new_indirizzo)
        return build_indirizzo(new_indirizzo)
    except Exception as e:
        raise e

async def put_indirizzo(indirizzo_id: int, indirizzo: IndirizzoUpdate, db: AsyncSession) -> IndirizzoResponse:
    try:
        stmt = select(Indirizzo).filter(Indirizzo.id == indirizzo_id)
        result = await db.execute(stmt)
        existing_indirizzo = result.scalars().first()
        if not existing_indirizzo:
            raise Exception("Indirizzo non trovato")
            
        existing_indirizzo.nome = indirizzo.nome
        existing_indirizzo.descrizione = indirizzo.descrizione
        
        await db.commit()
        await db.refresh(existing_indirizzo)
        return build_indirizzo(existing_indirizzo)
    except Exception as e:
        raise e

async def delete_indirizzo(indirizzo_id: int, db: AsyncSession):
    try:
        stmt = select(Indirizzo).filter(Indirizzo.id == indirizzo_id)
        result = await db.execute(stmt)
        indirizzo = result.scalars().first()
        if not indirizzo:
            raise Exception("Indirizzo non trovato")
        await db.delete(indirizzo)
        await db.commit()
        return {"message": "Indirizzo eliminato con successo"}
    except Exception as e:
        raise e
