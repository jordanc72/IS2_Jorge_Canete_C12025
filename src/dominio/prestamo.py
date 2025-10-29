from dataclasses import dataclass
from typing import Optional


@dataclass
class Prestamo:
    id: Optional[int]
    id_socio: int
    id_libro: int
    devuelto: bool = False

    