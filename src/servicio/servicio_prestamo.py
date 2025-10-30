from data.repositorios_prueba import InMemoryDB
from dominio.prestamo import Prestamo


class ServicioPrestamo:
    MAX_PRESTAMOS = 3


    def __init__(self, db: InMemoryDB):
        self.db = db


    def puede_prestar(self, id_socio: int) -> bool:
        m = self.db.get_member(id_socio)
        if not m:
            return False
        return m.active_loans < ServicioPrestamo.MAX_PRESTAMOS


    def prestar(self, id_socio: int, id_libro: int) -> bool:
        print(f"[DEBUG ServicioPrestamo] prestar llamado con socio_id={id_socio}, libro_id={id_libro}")
        member = self.db.get_member(id_socio)
        book = self.db.get_book(id_libro)
        if member is None or book is None:
            print("socio o libro no encontrado")
            return False
        
        # crear préstamo
        lr = self.db.insert_loan(id_socio, id_libro)
        self.db.update_member_loans(id_socio, member.active_loans + 1)
        self.db.update_book_copies(id_libro, book.copies - 1)

        # devolver el id del préstamo creado (truthy si éxito)
        return lr.id


    def devolver(self, id_prestamo: int) -> bool:
        try:
            print(f"[DEBUG ServicioPrestamo] devolver llamado con loan_id={id_prestamo}")
            loan = self.db.get_loan(id_prestamo)
            if loan is None:
                print("préstamo no encontrado")
                return False

            if getattr(loan, 'returned', False):
                print("préstamo ya devuelto")
                return False

            # actualizar libro y socio vía repo
            ok_inc = self.db.increment_copies(loan.book_id)
            ok_close = self.db.close_loan(id_prestamo)

            member = self.db.get_member(loan.member_id)
            if member is not None and hasattr(member, 'active_loans'):
                member.active_loans = max(0, member.active_loans - 1)
            
            return ok_inc and ok_close
        except Exception as e:
            print(f"[ERROR ServicioPrestamo] excepción en devolver: {e}")
            return False