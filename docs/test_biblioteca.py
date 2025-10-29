import unittest
from biblioteca import ConexionDB, LibroDAO, SocioDAO, PrestamoDAO, GestorBiblioteca
from datetime import datetime, timedelta


class TestBiblioteca(unittest.TestCase):
    def setUp(self):
    # Reiniciar la instancia de BD entre tests
        ConexionDB._instancia = None
        self.gestor = GestorBiblioteca()
        self.libdao = LibroDAO()
        self.sociodao = SocioDAO()
        self.prestdao = PrestamoDAO()
        # crear datos base
        self.sid = self.sociodao.crear('Ana')
        self.lid = self.libdao.crear('Programación 101', 1)


    # Prueba unitaria 1: caja negra — préstamo exitoso
    def test_prestamo_exitoso(self):
        ok, pid = self.gestor.prestar_libro(self.sid, self.lid)
        self.assertTrue(ok)
        self.assertIsInstance(pid, int)