from dataclasses import dataclass
from typing import Optional


@dataclass
class Socio:
    id: Optional[int]
    nombre: str
    prestamos_activos: int = 0

    