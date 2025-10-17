from __future__ import annotations

from typing import Optional

from app.api.deps import get_db
from app.models import Scuola, Citta
from app.schemas.school import SchoolsList, SchoolBase, SchoolAddress


async def get_schools(
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
        db = next(get_db())
        query = db.query(Scuola).join(Scuola.citta)
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
            "citta": Scuola.citta.has(),
            "provincia": Scuola.citta.has()
        }.get(sort_by, Scuola.nome)
        if order == "desc":
            sort_column = sort_column.desc()
        query = query.order_by(sort_column)
        total = query.count()
        scuole = query.offset(offset).limit(limit).all()

        def build_school(scuola):

            def build_address(addr):
                return SchoolAddress(
                    nome=addr.nome,
                    descrizione=addr.descrizione,
                    materie=[m.nome for m in addr.materie],
                )

            return SchoolBase(
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
        raise e
