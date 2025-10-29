from dataclasses import dataclass
from typing import Optional


@dataclass
class Libro:
    id: Optional[int]
    titulo: str
    copias: int