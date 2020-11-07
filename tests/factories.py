import factory
import random

from python_solid_principles.product_management_system.employees.entities import (
    Employee,
)
from python_solid_principles.product_management_system.products.entities import Product
from python_solid_principles.product_management_system.sales.entities import Sale


class ProductFactory(factory.Factory):
    class Meta:
        model = Product

    id_ = factory.Faker("pyint")
    name = factory.Faker("sentence")
    country_of_origin = factory.Faker("country_code")
    price = factory.LazyFunction(lambda: random.randint(1, 10000) / 100)


class EmployeeFactory(factory.Factory):
    class Meta:
        model = Employee

    id_ = factory.Faker("pyint")
    name = factory.Faker("name")
    manager = None


class SaleFactory(factory.Factory):
    class Meta:
        model = Sale

    product = factory.SubFactory(ProductFactory)
    quantity = factory.LazyFunction(lambda: random.randint(1, 100))
    time_of_sale = factory.Faker("date_object")
    sold_by = factory.SubFactory(EmployeeFactory)
