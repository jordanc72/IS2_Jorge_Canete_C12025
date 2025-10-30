import unittest
from data.repositorios_prueba import InMemoryDB
from servicio.servicio_libro import ServicioLibro
from servicio.servicio_socio import ServicioSocio
from servicio.servicio_prestamo import ServicioPrestamo

class TestBiblioteca(unittest.TestCase):
    def setUp(self):
        self.db = InMemoryDB()
        self.slib = ServicioLibro(self.db)
        self.ssoc = ServicioSocio(self.db)
        self.spre = ServicioPrestamo(self.db)
        # datos iniciales
        self.b1 = self.slib.crear_libro("Clean Code", 2)
        self.b2 = self.slib.crear_libro("No Stock", 0)
        self.m1 = self.ssoc.crear_socio("Ana")
        self.m2 = self.ssoc.crear_socio("Luis")

    # Black-box
    def test_bb_borrow_success(self):
        ok = self.spre.prestar(self.m1.id, self.b1.id)
        self.assertTrue(ok)
        mb = self.db.get_member(self.m1.id)
        bb = self.db.get_book(self.b1.id)
        self.assertEqual(mb.active_loans, 1)
        self.assertEqual(bb.copies, 1)
    
    def test_bb_borrow_no_copies(self):
        ok = self.spre.prestar(self.m1.id, self.b2.id)
        self.assertFalse(ok)

    # White-box
    def test_wb_max_loans_prevents(self):
        # ejemplo: llenar hasta MAX_PRESTAMOS con prestamos válidos
        for i in range(ServicioPrestamo.MAX_PRESTAMOS):
            b = self.slib.crear_libro(f"Temp{i}", 1)
            self.assertTrue(self.spre.prestar(self.m2.id, b.id))
        self.assertFalse(self.spre.prestar(self.m2.id, self.b1.id))

    def test_wb_return_updates(self):
        self.assertTrue(self.spre.prestar(self.m1.id, self.b1.id))
        loans = self.db.find_active_loans_by_member(self.m1.id)
        self.assertTrue(len(loans) >= 1)
        loan_id = loans[0].id
        self.assertTrue(self.spre.devolver(loan_id))
        m = self.db.get_member(self.m1.id)
        b = self.db.get_book(self.b1.id)
        self.assertEqual(m.active_loans, 0)
        self.assertEqual(b.copies, 2)

    # Boundary
    def test_boundary_max_minus_one_allows(self):
        self.db.update_member_loans(self.m1.id, ServicioPrestamo.MAX_PRESTAMOS - 1)
        self.assertTrue(self.spre.prestar(self.m1.id, self.b1.id))


    def test_boundary_at_max_disallows(self):
        self.db.update_member_loans(self.m1.id, ServicioPrestamo.MAX_PRESTAMOS)
        self.assertFalse(self.spre.prestar(self.m1.id, self.b1.id))


    # Unit tests
    def test_unit_puede_prestar(self):
        self.db.update_member_loans(self.m1.id, 0)
        self.assertTrue(self.spre.puede_prestar(self.m1.id))
        self.db.update_member_loans(self.m1.id, ServicioPrestamo.MAX_PRESTAMOS)
        self.assertFalse(self.spre.puede_prestar(self.m1.id))


    def test_unit_create_and_get_book(self):
        b = self.slib.crear_libro("Nuevo", 5)
        row = self.db.get_book(b.id)
        self.assertEqual(row.title, "Nuevo")
        self.assertEqual(row.copies, 5)


if __name__ == '__main__':
    unittest.main()