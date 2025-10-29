import sqlite3
from datetime import datetime, timedelta


class ConexionDB:
    _instancia = None


    def __init__(self):
        raise RuntimeError('Use get_instancia()')


    @classmethod
    def get_instancia(cls):
        if cls._instancia is None:
            cls._instancia = cls.__crear_instancia()
        return cls._instancia


    @classmethod
    def __crear_instancia(cls):
        obj = object.__new__(cls)
        obj.conn = sqlite3.connect(':memory:')
        obj.conn.row_factory = sqlite3.Row
        cls.__inicializar_schema(obj.conn)
        return obj


    @staticmethod
    def __inicializar_schema(conn):
        cur = conn.cursor()
        cur.execute('''
        CREATE TABLE socio (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL
        )
        ''')
        cur.execute('''
        CREATE TABLE libro (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT NOT NULL,
        ejemplares INTEGER NOT NULL
        )
        ''')
        cur.execute('''
        CREATE TABLE prestamo (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        socio_id INTEGER,
        libro_id INTEGER,
        fecha_prestamo TEXT,
        fecha_limite TEXT,
        fecha_devolucion TEXT,
        FOREIGN KEY(socio_id) REFERENCES socio(id),
        FOREIGN KEY(libro_id) REFERENCES libro(id)
        )
        ''')
        conn.commit()

class LibroDAO:
    def __init__(self):
        self.conn = ConexionDB.get_instancia().conn


    def crear(self, titulo, ejemplares):
        cur = self.conn.cursor()
        cur.execute('INSERT INTO libro (titulo, ejemplares) VALUES (?, ?)', (titulo, ejemplares))
        self.conn.commit()
        return cur.lastrowid


    def obtener(self, libro_id):
        cur = self.conn.cursor()
        cur.execute('SELECT * FROM libro WHERE id=?', (libro_id,))
        return cur.fetchone()


    def decrementar_ejemplar(self, libro_id):
        cur = self.conn.cursor()
        cur.execute('UPDATE libro SET ejemplares = ejemplares - 1 WHERE id=? AND ejemplares>0', (libro_id,))
        self.conn.commit()
        return cur.rowcount == 1


    def incrementar_ejemplar(self, libro_id):
        cur = self.conn.cursor()
        cur.execute('UPDATE libro SET ejemplares = ejemplares + 1 WHERE id=?', (libro_id,))
        self.conn.commit()
        return cur.rowcount == 1

class SocioDAO:
    def __init__(self):
        self.conn = ConexionDB.get_instancia().conn


    def crear(self, nombre):
        cur = self.conn.cursor()
        cur.execute('INSERT INTO socio (nombre) VALUES (?)', (nombre,))
        self.conn.commit()
        return cur.lastrowid


    def prestamos_activos(self, socio_id):
        cur = self.conn.cursor()
        cur.execute('SELECT COUNT(*) as c FROM prestamo WHERE socio_id=? AND fecha_devolucion IS NULL', (socio_id,))
        return cur.fetchone()['c']

class PrestamoDAO:
    def __init__(self):
        self.conn = ConexionDB.get_instancia().conn


    def crear(self, socio_id, libro_id, fecha_prestamo, fecha_limite):
        cur = self.conn.cursor()
        cur.execute('''INSERT INTO prestamo (socio_id, libro_id, fecha_prestamo, fecha_limite) VALUES (?,?,?,?)
        ''', (socio_id, libro_id, fecha_prestamo.isoformat(), fecha_limite.isoformat()))
        self.conn.commit()
        return cur.lastrowid


    def cerrar(self, prestamo_id, fecha_devolucion):
        cur = self.conn.cursor()
        cur.execute('UPDATE prestamo SET fecha_devolucion=? WHERE id=?', (fecha_devolucion.isoformat(), prestamo_id))
        self.conn.commit()
        return cur.rowcount == 1


    def obtener(self, prestamo_id):
        cur = self.conn.cursor()
        cur.execute('SELECT * FROM prestamo WHERE id=?', (prestamo_id,))
        row = cur.fetchone()
        return row


class GestorBiblioteca:
    MAX_PRESTAMOS = 3


    def __init__(self):
        self.libro_dao = LibroDAO()
        self.socio_dao = SocioDAO()
        self.prestamo_dao = PrestamoDAO()


    def prestar_libro(self, socio_id, libro_id):
        # Validaciones de negocio
        if self.socio_dao.prestamos_activos(socio_id) >= GestorBiblioteca.MAX_PRESTAMOS:
            return False, 'Límite de préstamos alcanzado'
        if not self.libro_dao.decrementar_ejemplar(libro_id):
            return False, 'No hay ejemplares disponibles'
        f_prest = datetime.now()
        f_limite = f_prest + timedelta(days=14)
        pid = self.prestamo_dao.crear(socio_id, libro_id, f_prest, f_limite)
        return True, pid


    def devolver_libro(self, prestamo_id):
        row = self.prestamo_dao.obtener(prestamo_id)
        if not row:
            return False, 'Préstamo no encontrado'
        if row['fecha_devolucion'] is not None:
            return False, 'Préstamo ya devuelto'
        fecha_limite = datetime.fromisoformat(row['fecha_limite'])
        fecha_devol = datetime.now()
        dias_retraso = (fecha_devol - fecha_limite).days
        multa = self._calcular_multa(dias_retraso)
        ok = self.prestamo_dao.cerrar(prestamo_id, fecha_devol)
        self.libro_dao.incrementar_ejemplar(row['libro_id'])
        return ok, multa


    def _calcular_multa(self, dias_retraso):
        # regla simple: $10 por día de atraso, 0 si <=0
        if dias_retraso <= 0:
            return 0
        return dias_retraso * 10