from abc import abstractmethod
from typing import Protocol

from python_solid_principles.jas.sales.entities import Sale


class SalesValidator(Protocol):
    @abstractmethod
    def validate(self, sale: Sale) -> None:
        ...
