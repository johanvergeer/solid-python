from python_solid_principles.jas.sales.entities import Sale
from python_solid_principles.jas.sales.repositories import SalesRepository
from python_solid_principles.jas.sales.validation import SalesValidator


def add_sale(sale: Sale) -> None:
    repo = SalesRepository()
    validator = SalesValidator()

    validator.validate(sale)
    repo.add(sale)
