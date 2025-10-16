from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

def import_models():
    from app.models import Citta, Materia, Indirizzo, Scuola # noqa: E402 F401