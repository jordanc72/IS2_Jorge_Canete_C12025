from src.data.repositorios_prueba import InMemoryDB
from src.dominio.socio import Socio


class ServicioSocios:
    def __init__(self, db: InMemoryDB):
        self.db = db


    def crear_socio(self, nombre: str) -> Socio:
        r = self.db.insert_member(nombre)
        return Socio(id=r.id, nombre=r.name, prestamos_activos=r.active_loans)


    def obtener_socio(self, id_socio: int) -> Socio | None:
        r = self.db.get_member(id_socio)
        if not r:
            return None
        return Socio(id=r.id, nombre=r.name, prestamos_activos=r.active_loans)