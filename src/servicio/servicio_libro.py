from src.data.repositorios_prueba import InMemoryDB
from src.dominio.libro import Libro


class ServicioLibro:
    def __init__(self, db: InMemoryDB):
        self.db = db


    def crear_libro(self, titulo: str, copias: int) -> Libro:
        row = self.db.insert_book(titulo, copias)
        return Libro(id=row.id, titulo=row.title, copias=row.copies)


    def obtener_libro(self, id_libro: int) -> Libro | None:
        r = self.db.get_book(id_libro)
        if not r:
            return None
        return Libro(id=r.id, titulo=r.title, copias=r.copies)