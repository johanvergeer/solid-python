from abc import abstractmethod
from datetime import date
from typing import Protocol, Set

from python_solid_principles.jas.sales.entities import Sale


class SalesRepository(Protocol):
    @abstractmethod
    def find_from_to_date(self, from_date: date, to_date: date) -> Set[Sale]:
        """Find all sales starting at from_date until to_date"""
        ...

    @abstractmethod
    def add(self, sale: Sale) -> None:
        ...


class SalesRepositoryImpl(SalesRepository):
    def find_from_to_date(self, from_date: date, to_date: date) -> Set[Sale]:
        pass

    def add(self, sale: Sale) -> None:
        pass


def sales_repository_factory() -> SalesRepository:
    return SalesRepositoryImpl()
