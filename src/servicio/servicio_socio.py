from data.repositorios_prueba import InMemoryDB
from dominio.socio import Socio


class ServicioSocio:
    def __init__(self, db: InMemoryDB):
        self.db = db


    def crear_socio(self, nombre: str) -> Socio:
        socio_id = self.db.create_member(nombre)
        return self.db.get_member(socio_id)


    def obtener_socio(self, id_socio: int) -> Socio | None:
        r = self.db.get_member(id_socio)
        if not r:
            return None
        return Socio(id=r.id, nombre=r.name, prestamos_activos=r.active_loans)