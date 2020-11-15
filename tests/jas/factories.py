import random

import factory

from python_solid_principles.jas.employees.entities import Employee
from python_solid_principles.jas.products.entities import Product
from python_solid_principles.jas.resellers.entities import Reseller
from python_solid_principles.jas.sales.entities import Sale, InternalSale, ExternalSale


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


class ResellerFactory(factory.Factory):
    class Meta:
        model = Reseller

    id_ = factory.Faker("pyint")
    name = factory.Faker("name")
    contact = factory.SubFactory(EmployeeFactory)


class SaleFactory(factory.Factory):
    class Meta:
        model = Sale

    product = factory.SubFactory(ProductFactory)
    quantity = factory.LazyFunction(lambda: random.randint(1, 100))
    time_of_sale = factory.Faker("date_object")


class InternalSaleFactory(SaleFactory):
    class Meta:
        model = InternalSale
    sold_by = factory.SubFactory(EmployeeFactory)


class ExternalSaleFactory(SaleFactory):
    class Meta:
        model = ExternalSale
    sold_by = factory.SubFactory(ResellerFactory)
