 El diseño arquitectónico lo podemos separar en 3 capas fundamentales que detallaremos más adelante. 

El patrón elegido para acceso centralizado a BD es el Singleton, con su implementación y validación en Python (modelo sencillo con SQLite in-memory).

# Identificación de capas

1) Capas principales y funciones

* Capa de Presentación

Función: interactuar con el usuario (CLI/web).

Funciones genéricas:

mostrar_libros_disponibles()

form_alta_socio()

form_prestamo()

buscar_por_titulo()

* Capa de Lógica de Negocio

Función: formalizar las reglas del dominio (préstamos, devoluciones, multas).

Funciones genérica:

prestar_libro(socio_id, libro_id) — valida reglas (máx 3 préstamos activos).

devolver_libro(prestamo_id) — calcula multa si corresponde.

calcular_multa(fecha_devolucion, fecha_limite) — regla interna.

* Capa de Datos

Función: persistencia y acceso (DAOs).

Componentes:

ConexionDB (Singleton) — punto central de conexión.

LibroDAO, SocioDAO, PrestamoDAO — CRUD y consultas.

# Relación de capas

<img src="./Patron-Modelo-Arquitectónico.drawio.png">