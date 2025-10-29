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
        m = self.db.get_member(id_socio)
        b = self.db.get_book(id_libro)
        if not m or not b:
            return False
        if m.active_loans >= ServicioPrestamo.MAX_PRESTAMOS:
            return False
        if b.copies <= 0:
            return False
        # crear préstamo
        lr = self.db.insert_loan(id_socio, id_libro)
        self.db.update_member_loans(id_socio, m.active_loans + 1)
        self.db.update_book_copies(id_libro, b.copies - 1)
        return True


    def devolver(self, id_prestamo: int) -> bool:
        loan = self.db.get_loan(id_prestamo)
        if not loan or loan.returned:
           return False
        self.db.mark_loan_returned(id_prestamo)
        member = self.db.get_member(loan.member_id)
        book = self.db.get_book(loan.book_id)
        self.db.update_member_loans(member.id, member.active_loans - 1)
        self.db.update_book_copies(book.id, book.copies + 1)
        return True