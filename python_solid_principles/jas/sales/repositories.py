from datetime import date
from typing import Protocol, Set

from python_solid_principles.jas.sales.entities import Sale


class SalesRepository(Protocol):
    def find_from_to_date(self, from_date: date, to_date: date) -> Set[Sale]:
        """Find all sales starting at from_date until to_date"""
        ...
