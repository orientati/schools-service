from __future__ import annotations
from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.models import Materia, Indirizzo
from app.schemas.materia import MateriaList, MateriaResponse, MateriaUpdate

def build_materia(materie) -> MateriaResponse:
    return MateriaResponse(
        id=materie.id,
        nome=materie.nome,
        descrizione=materie.descrizione
    )

async def get_materie(
        db: AsyncSession,
        limit: int,
        offset: int,
        search: Optional[str],
        sort_by: Optional[str],
        order: Optional[str]
) -> MateriaList:
    try:
        stmt = select(Materia)
        if search:
            stmt = stmt.filter(Materia.nome.ilike(f"%{search}%"))
        
        sort_column = {
            "name": Materia.nome,
        }.get(sort_by, Materia.nome)
        
        if order == "desc":
            stmt = stmt.order_by(sort_column.desc())
        else:
            stmt = stmt.order_by(sort_column)

        result = await db.execute(stmt.offset(offset).limit(limit))
        materie = result.scalars().all()
        
        return MateriaList(
            total=len(materie), # Proxy
            limit=limit,
            offset=offset,
            materie=[build_materia(m) for m in materie],
            filter_search=search,
            sort_by=sort_by,
            order=order
        )
    except Exception as e:
        raise e

async def get_materia_by_id(materia_id: int, db: AsyncSession) -> MateriaResponse:
    try:
        stmt = select(Materia).filter(Materia.id == materia_id)
        result = await db.execute(stmt)
        materia = result.scalars().first()
        if not materia:
            raise Exception(f"Materia con ID {materia_id} non trovata.")
        return build_materia(materia)
    except Exception as e:
        raise e

async def create_materia(materia_data: MateriaResponse, db: AsyncSession) -> MateriaResponse:
    try:
        nuova_materia = Materia(
            nome=materia_data.nome,
            descrizione=materia_data.descrizione
        )
        db.add(nuova_materia)
        await db.commit()
        await db.refresh(nuova_materia)
        return build_materia(nuova_materia)
    except Exception as e:
        raise e

async def update_materia(materia_id: int, materia_data: MateriaUpdate, db: AsyncSession) -> MateriaResponse:
    try:
        stmt = select(Materia).filter(Materia.id == materia_id)
        result = await db.execute(stmt)
        materia = result.scalars().first()
        if not materia:
            raise Exception(f"Materia con ID {materia_id} non trovata.")
        materia.nome = materia_data.nome
        materia.descrizione = materia_data.descrizione
        await db.commit()
        await db.refresh(materia)
        return build_materia(materia)
    except Exception as e:
        raise e

async def delete_materia(materia_id: int, db: AsyncSession):
    try:
        stmt = select(Materia).options(selectinload(Materia.indirizzi)).filter(Materia.id == materia_id)
        result = await db.execute(stmt)
        materia = result.scalars().first()
        if not materia:
            raise Exception(f"Materia con ID {materia_id} non trovata.")
        if materia.indirizzi:
            raise Exception(
                f"Impossibile eliminare la materia con ID {materia_id} perché collegata a uno o più indirizzi di studio.")
        await db.delete(materia)
        await db.commit()
        return {"message": f"Materia {materia_id} eliminata con successo."}
    except Exception as e:
        raise e

async def link_materia_to_indirizzo(materia_id: int, indirizzo_id: int, db: AsyncSession):
    try:
        stmt = select(Materia).options(selectinload(Materia.indirizzi)).filter(Materia.id == materia_id)
        result = await db.execute(stmt)
        materia = result.scalars().first()
        if not materia:
            raise Exception(f"Materia con ID {materia_id} non trovata.")
            
        stmt_addr = select(Indirizzo).filter(Indirizzo.id == indirizzo_id)
        result_addr = await db.execute(stmt_addr)
        indirizzo = result_addr.scalars().first()
        if not indirizzo:
            raise Exception(f"Indirizzo con ID {indirizzo_id} non trovato.")
            
        if indirizzo in materia.indirizzi:
            raise Exception(f"Indirizzo con ID {indirizzo_id} già collegato alla materia con ID {materia_id}.")
            
        materia.indirizzi.append(indirizzo)
        await db.commit()
        await db.refresh(materia)
        return build_materia(materia)
    except Exception as e:
        raise e

async def unlink_materia_from_indirizzo(materia_id: int, indirizzo_id: int, db: AsyncSession):
    try:
        stmt = select(Materia).options(selectinload(Materia.indirizzi)).filter(Materia.id == materia_id)
        result = await db.execute(stmt)
        materia = result.scalars().first()
        if not materia:
            raise Exception(f"Materia con ID {materia_id} non trovata.")
            
        stmt_addr = select(Indirizzo).filter(Indirizzo.id == indirizzo_id)
        result_addr = await db.execute(stmt_addr)
        indirizzo = result_addr.scalars().first()
        if not indirizzo:
            raise Exception(f"Indirizzo con ID {indirizzo_id} non trovato.")
            
        if indirizzo not in materia.indirizzi:
            raise Exception(f"Indirizzo con ID {indirizzo_id} non collegato alla materia con ID {materia_id}.")
            
        materia.indirizzi.remove(indirizzo)
        await db.commit()
        await db.refresh(materia)
        return build_materia(materia)
    except Exception as e:
        raise e
