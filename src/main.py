# main.py

from servicio.servicio_libro import ServicioLibro
from servicio.servicio_socio import ServicioSocio
from servicio.servicio_prestamo import ServicioPrestamo
from data.repositorios_prueba import InMemoryDB
from presentacion.vista import Vista

def main():
    
    db = InMemoryDB()
    vista = Vista(db)
    servicio_libro = ServicioLibro(db)
    servicio_socio = ServicioSocio(db)
    servicio_prestamo = ServicioPrestamo(db)

    while True:
        opcion = vista.mostrar_menu()

        if opcion == '1':
            titulo, ejemplares = vista.ingresar_libro()
            servicio_libro.crear_libro(titulo, ejemplares)
            print("Libro agregado correctamente.\n")

        elif opcion == '2':
            nombre = vista.ingresar_socio()
            servicio_socio.crear_socio(nombre)
            print("Socio registrado correctamente.\n")

        elif opcion == '3':
            socio_id, libro_id = vista.realizar_prestamo()
            print(f"[DEBUG] llamar a prestar: socio_id={socio_id}, libro_id={libro_id}")
            loan_id = servicio_prestamo.prestar(socio_id, libro_id)
            print(f"[DEBUG] prestar() devolvió: {loan_id}")
            if loan_id:
                print(f"Préstamo registrado con éxito. ID préstamo: {loan_id}\n")
            else:
                print("Error: Libro no disponible o socio inexistente.\n")

        elif opcion == '4':
            loan_id = vista.realizar_devolucion()
            exito = servicio_prestamo.devolver(loan_id)
            if exito:
                print("Devolución realizada con éxito.\n")
            else:
                print("Error: No se encontró el préstamo o ya estaba devuelto.\n")

        elif opcion == '5':
            print("Saliendo del sistema...")
            break

        else:
            print("Opción inválida, intente nuevamente.\n")


if __name__ == "__main__":
    main()
