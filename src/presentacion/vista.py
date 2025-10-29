from servicio.servicio_libro import ServicioLibro
from servicio.servicio_socios import ServicioSocios
from servicio.servicio_prestamo import ServicioPrestamo
from data.repositorios_prueba import InMemoryDB


class Vista:
    def __init__(self, db: InMemoryDB):
        self.db = db
        self.s_libro = ServicioLibro(db)
        self.s_socios = ServicioSocios(db)
        self.s_prestamo = ServicioPrestamo(db)


    def menu_simple(self):
        print("1) Crear socio\n2) Crear libro\n3) Prestar libro\n4) Devolver libro\n5) Salir")