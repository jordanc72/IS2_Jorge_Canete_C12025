from servicio.servicio_libro import ServicioLibro
from servicio.servicio_socio import ServicioSocio
from servicio.servicio_prestamo import ServicioPrestamo
from data.repositorios_prueba import InMemoryDB


class Vista:
    def __init__(self, db: InMemoryDB):
        self.db = db
        self.s_libro = ServicioLibro(db)
        self.s_socio = ServicioSocio(db)
        self.s_prestamo = ServicioPrestamo(db)


    def menu_simple(self):
        print("1) Crear libro\n2) Crear socio\n3) Prestar libro\n4) Devolver libro\n5) Salir")

    def mostrar_menu(self) -> str:
        self.menu_simple()
        return input("Seleccione una opción: ").strip()

    def ingresar_libro(self) -> tuple:
        titulo = input("Título del libro: ").strip()
        while True:
            try:
                ejemplares = int(input("Número de ejemplares: ").strip())
                break
            except ValueError:
                print("Ingrese un número entero válido para ejemplares.")
        return titulo, ejemplares

    def ingresar_socio(self) -> str:
        nombre = input("Nombre del socio: ").strip()
        return nombre

    def realizar_prestamo(self) -> tuple:
        while True:
            try:
                socio_id = int(input("ID del socio: ").strip())
                libro_id = int(input("ID del libro: ").strip())
                return socio_id, libro_id
            except ValueError:
                print("IDs deben ser enteros. Intente de nuevo.")

    def realizar_devolucion(self) -> int:
        while True:
            try:
                loan_id = int(input("ID del préstamo a devolver: ").strip())
                return loan_id
            except ValueError:
                print("ID inválido. Ingrese un entero.")