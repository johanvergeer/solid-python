from datetime import datetime

from python_solid_principles.product_management_system.employees.entities import (
    Employee,
)
from python_solid_principles.product_management_system.products.entities import Product


class Sale:
    def __init__(
        self, product: Product, quantity: int, time_of_sale: datetime, sold_by: Employee
    ) -> None:
        self.__product = product
        self.__quantity = quantity
        self.__time_of_sale = time_of_sale
        self.__sold_by = sold_by

    @property
    def id(self) -> str:
        return f"{self.__product.id}_{self.__sold_by.id}_{self.__time_of_sale}"

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
    def sold_by(self) -> Employee:
        return self.__sold_by

    @property
    def total(self) -> float:
        return self.__product.price * self.__quantity
