"""
Adatforrások betöltése:
- source_a: Steam CSV-k (A forrás)
- source_b: JSON adatok (B forrás)
- source_c: Egyesített CSV-k (C forrás)
"""

from .source_a import *
from .source_b import *
from .source_c import *

__all__ = ["source_a", "source_b", "source_c"]
