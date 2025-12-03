from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

def import_models():
    from app.models import Citta
    from app.models import Scuola
    from app.models import Indirizzo
    from app.models import Materia
