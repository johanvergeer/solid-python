from python_solid_principles.jas.sales.entities import Sale
from python_solid_principles.jas.sales.repositories import SalesRepository
from python_solid_principles.jas.sales.validation import SalesValidator


def add_sale(sale: Sale, repo: SalesRepository, validator: SalesValidator) -> None:
    validator.validate(sale)
    repo.add(sale)
