from abc import ABC, abstractmethod
from datetime import datetime

from python_solid_principles.jas.employees.entities import Employee
from python_solid_principles.jas.products.entities import Product
from python_solid_principles.jas.resellers.entities import Reseller


class Sale(ABC):
    def __init__(self, product: Product, quantity: int, time_of_sale: datetime) -> None:
        self.__product = product
        self.__quantity = quantity
        self.__time_of_sale = time_of_sale

    @property
    @abstractmethod
    def id(self) -> str:
        """Unique identifier for the sale"""
        ...

    @property
    def product(self) -> Product:
        return self.__product

    @property
    def quantity(self) -> int:
        return self.__quantity

    @property
    def time_of_sale(self) -> datetime:
        return self.__time_of_sale

    @property
    def total(self) -> float:
        return self.__product.price * self.__quantity

    @property
    @abstractmethod
    def sold_by_name(self) -> str:
        ...

    @property
    @abstractmethod
    def sold_by_manager_name(self) -> str:
        ...


class InternalSale(Sale):
    def __init__(
        self, product: Product, quantity: int, time_of_sale: datetime, sold_by: Employee
    ) -> None:
        super(InternalSale, self).__init__(product, quantity, time_of_sale)
        self.__sold_by = sold_by

    @property
    def id(self) -> str:
        return f"{self.__product.id}_{self.__sold_by.id}_{self.__time_of_sale}"

    @property
    def sold_by(self) -> Employee:
        return self.__sold_by

    @property
    def sold_by_name(self) -> str:
        return self.__sold_by.name

    @property
    def sold_by_manager_name(self) -> str:
        return self.__sold_by.manager.name


class ExternalSale(Sale):
    def __init__(
        self, product: Product, quantity: int, time_of_sale: datetime, sold_by: Reseller
    ) -> None:
        super(ExternalSale, self).__init__(product, quantity, time_of_sale)
        self.__sold_by = sold_by

    @property
    def id(self) -> str:
        return f"{self.__product.id}_{self.__sold_by.id}_{self.__time_of_sale}"

    @property
    def sold_by(self) -> Reseller:
        return self.__sold_by

    @property
    def sold_by_name(self) -> str:
        return self.__sold_by.name

    @property
    def sold_by_manager_name(self) -> str:
        return self.__sold_by.contact.name
