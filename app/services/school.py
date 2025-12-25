from __future__ import annotations

from typing import Optional

from sqlalchemy import select, func, asc, desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from app.api.deps import get_db
from app.models import Scuola, Citta, Indirizzo
from app.schemas.school import SchoolsList, SchoolResponse, SchoolAddress, SchoolCreate, SchoolDeleteResponse
from app.services.http_client import OrientatiException


def build_school(scuola: Scuola) -> SchoolResponse:
    def build_address(addr):
        return SchoolAddress(
            id=addr.id,
            nome=addr.nome,
            descrizione=addr.descrizione,
            materie=[m.nome for m in addr.materie],
        )

    return SchoolResponse(
        id=scuola.id,
        nome=scuola.nome,
        tipo=scuola.tipo,
        indirizzo=scuola.indirizzo,
        città=scuola.citta.nome,
        provincia=scuola.citta.provincia,
        codice_postale=scuola.citta.codice_postale,
        email_contatto=scuola.email,
        telefono_contatto=scuola.telefono,
        indirizzi_scuola=[build_address(addr) for addr in scuola.indirizzi],
        sito_web=scuola.sito_web,
        descrizione=scuola.descrizione,
        created_at=scuola.created_at,
        updated_at=scuola.updated_at
    )


async def get_schools(
        db: AsyncSession,
        limit: int = 10,
        offset: int = 0,
        search: Optional[str] = None,
        tipo: Optional[str] = None,
        citta: Optional[str] = None,
        provincia: Optional[str] = None,
        indirizzo: Optional[str] = None,
        sort_by: str = "name",
        order: str = "asc"
) -> SchoolsList:
    """
    Recupera la lista delle scuole con opzioni di paginazione e filtro.

    Args:
        db (AsyncSession): Sessione del database.
        limit (int): Numero massimo di scuole da restituire.
        offset (int): Numero di scuole da saltare per la paginazione.
        search (Optional[str]): Termine di ricerca per filtrare le scuole per nome.
        tipo (Optional[str]): Filtra per tipo di scuola (es. Liceo, ITIS, ecc.).
        citta (Optional[str]): Filtra per città.
        provincia (Optional[str]): Filtra per provincia.
        indirizzo (Optional[str]): Filtra per tipo di studi (es. liceo classico, informatico, ecc.).
        sort_by (str): Campo per ordinamento (es. nome, città, provincia).
        order (str): Ordine: 'asc' o 'desc'.

    Returns:
        SchoolsList: Lista delle scuole con metadati di paginazione.
    """
    try:
        query = select(Scuola).join(Scuola.citta).options(
            joinedload(Scuola.citta),
            selectinload(Scuola.indirizzi).selectinload(Indirizzo.materie)
        )
        
        # applico i filtri
        if search:
            query = query.filter(Scuola.nome.ilike(f"%{search}%"))
        if tipo:
            query = query.filter(Scuola.tipo == tipo)
        if citta:
            query = query.filter(Citta.nome == citta)
        if provincia:
            query = query.filter(Citta.provincia == provincia)
        if indirizzo:
            query = query.filter(Scuola.indirizzo.ilike(f"%{indirizzo}%"))
            
        # applico l'ordinamento
        sort_column = {
            "name": Scuola.nome,
            "citta": Citta.nome,
            "provincia": Citta.provincia
        }.get(sort_by, Scuola.nome)
        
        if order == "desc":
            query = query.order_by(desc(sort_column))
        else:
            query = query.order_by(asc(sort_column))
        
        # Count query
        count_query = select(func.count()).select_from(Scuola).join(Scuola.citta)
        # Re-apply filters for count
        if search:
            count_query = count_query.filter(Scuola.nome.ilike(f"%{search}%"))
        if tipo:
            count_query = count_query.filter(Scuola.tipo == tipo)
        if citta:
            count_query = count_query.filter(Citta.nome == citta)
        if provincia:
            count_query = count_query.filter(Citta.provincia == provincia)
        if indirizzo:
            count_query = count_query.filter(Scuola.indirizzo.ilike(f"%{indirizzo}%"))

        total_result = await db.execute(count_query)
        total = total_result.scalar()

        result = await db.execute(query.offset(offset).limit(limit))
        scuole = result.scalars().all()

        return SchoolsList(
            total=total,
            limit=limit,
            offset=offset,
            scuole=[build_school(s) for s in scuole],
            filter_search=search,
            filter_tipo=tipo,
            filter_citta=citta,
            filter_provincia=provincia,
            filter_indirizzo=indirizzo,
            sort_by=sort_by,
            order=order
        )
    except Exception as e:
        raise OrientatiException(
            url="schools/get",
            exc=e
        )


async def get_school_by_id(school_id: int, db: AsyncSession):
    """
    Recupera una scuola per ID.

    Args:
        school_id (int): ID della scuola da recuperare.
        db (AsyncSession): Sessione DB.

    Returns:
        SchoolResponse: Dettagli della scuola.
    """
    try:
        stmt = select(Scuola).where(Scuola.id == school_id).options(
            joinedload(Scuola.citta),
            selectinload(Scuola.indirizzi).selectinload(Indirizzo.materie)
        )
        result = await db.execute(stmt)
        scuola = result.scalars().first()
        
        if not scuola:
            return None

        return build_school(scuola)

    except Exception as e:
        raise OrientatiException(
            url=f"schools/{school_id}",
            exc=e
        )


async def create_school(school: SchoolCreate, db: AsyncSession) -> SchoolResponse:
    """
    Crea una nuova scuola.

    Args:
        school (SchoolCreate): Dati della scuola da creare.
        db (AsyncSession): Sessione DB.

    Returns:
        SchoolResponse: Dettagli della scuola creata.
    """
    try:
        stmt = select(Citta).filter(Citta.id == school.citta_id)
        result = await db.execute(stmt)
        citta = result.scalars().first()

        if not citta:
            raise OrientatiException(
                status_code=404,
                url="schools/create",
                message="Not Found",
                details={"message": "City Not Found"}
            )

        nuova_scuola = Scuola(
            nome=school.nome,
            tipo=school.tipo,
            indirizzo=school.indirizzo,
            id_citta=citta.id,
            email=school.email_contatto,
            telefono=school.telefono_contatto,
            sito_web=school.sito_web,
            descrizione=school.descrizione
        )
        db.add(nuova_scuola)
        await db.commit()
        await db.refresh(nuova_scuola)
        
        # Re-fetch with relationships for response building
        return await get_school_by_id(nuova_scuola.id, db)

    except OrientatiException as e:
        raise e
    except Exception as e:
        raise OrientatiException(
            url="schools/create",
            exc=e
        )


def find_key(data: dict, target_key: str):
    """
    Cerca una chiave specifica in un dizionario annidato.

    :param data: Il dizionario in cui cercare.
    :param target_key: La chiave da cercare.
    :return:
    """

    for key, value in data.items():
        if key == target_key:
            return True
    return False


async def update_school(school_id: int, school: dict, db: AsyncSession) -> SchoolResponse:
    """
    Aggiorna una scuola esistente.

    Args:
        school_id (int): ID della scuola da aggiornare.
        school (dict): Dati aggiornati della scuola.
        db (AsyncSession): Sessione DB.

    Returns:
        SchoolResponse: Dettagli della scuola aggiornata.
    """
    try:
        stmt = select(Scuola).where(Scuola.id == school_id)
        result = await db.execute(stmt)
        scuola = result.scalars().first()

        if not scuola:
            raise OrientatiException(
                status_code=404,
                url=f"schools/{school_id}/update",
                message="Not Found",
                details={"message": "School Not Found"}
            )

        if not isinstance(school, dict):
            raise OrientatiException(
                status_code=400,
                url=f"schools/{school_id}/update",
                message="Bad Request",
                details={"message": "Invalid school data format"}
            )

        # Se ho un id di una citta, allora aggiorno la citta, senno no
        id_citta = school.get("citta_id", None)
        citta = None
        if id_citta is not None:
            stmt_citta = select(Citta).filter(Citta.id == school.get("citta_id", None))
            result_citta = await db.execute(stmt_citta)
            citta = result_citta.scalars().first()

            if not citta:
                raise OrientatiException(
                    status_code=404,
                    url=f"schools/{school_id}/update",
                    message="Not Found",
                    details={"message": "City Not Found"}
                )
        
        scuola.nome = school["nome"] if find_key(school, "nome") and school.get("nome",
                                                                                None) is not None else scuola.nome
        scuola.tipo = school["tipo"] if find_key(school, "tipo") and school.get("tipo",
                                                                                None) is not None else scuola.tipo
        scuola.indirizzo = school["indirizzo"] if find_key(school, "indirizzo") and school[
            "indirizzo"] else scuola.indirizzo
        scuola.id_citta = citta.id if id_citta is not None else scuola.id_citta
        scuola.email = school["email_contatto"] if find_key(school, "email_contatto") and school[
            "email_contatto"] is not None else scuola.email
        scuola.telefono = school["telefono_contatto"] if find_key(school, "telefono_contatto") and school[
            "telefono_contatto"] is not None else scuola.telefono
        scuola.sito_web = school["sito_web"] if find_key(school, "sito_web") else scuola.sito_web
        scuola.descrizione = school["descrizione"] if find_key(school, "descrizione") else scuola.descrizione

        await db.commit()
        await db.refresh(scuola)

        # Re-fetch for proper response with relations
        return await get_school_by_id(school_id, db)

    except OrientatiException as e:
        raise e
    except Exception as e:
        raise OrientatiException(
            url=f"schools/{school_id}/update",
            exc=e
        )


async def delete_school(school_id: int, db: AsyncSession) -> SchoolDeleteResponse:
    """
    Elimina una scuola esistente.

    Args:
        school_id (int): ID della scuola da eliminare.
        db (AsyncSession): Sessione DB.

    Returns:
        bool: True se la scuola è stata eliminata con successo, False altrimenti.
    """
    try:
        stmt = select(Scuola).where(Scuola.id == school_id)
        result = await db.execute(stmt)
        scuola = result.scalars().first()

        if not scuola:
            raise OrientatiException(
                status_code=404,
                url=f"schools/{school_id}/delete",
                message="Not Found",
                details={"message": "School Not Found"}
            )

        await db.delete(scuola)
        await db.commit()

        return SchoolDeleteResponse()

    except OrientatiException as e:
        raise e
    except Exception as e:
        raise OrientatiException(
            url=f"schools/{school_id}/delete",
            exc=e
        )
