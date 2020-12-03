from python_solid_principles.jas.sales.entities import Sale
from python_solid_principles.jas.sales.repositories import sales_repository_factory
from python_solid_principles.jas.sales.validation import sales_validator_factory


def add_sale(sale: Sale) -> None:
    repo = sales_repository_factory()
    validator = sales_validator_factory()

    validator.validate(sale)
    repo.add(sale)
