from datetime import datetime
from pathlib import Path

import pytest

from python_solid_principles.product_management_system.sales.entities import Sale
from python_solid_principles.product_management_system.sales.reports import (
    create_sales_report,
)
from python_solid_principles.product_management_system.sales.repositories import (
    SalesRepository,
)
from tests.factories import SaleFactory


@pytest.fixture
def sales_repo_mock(mocker):
    return mocker.MagicMock(name="repo_mock", spec=SalesRepository)


def test_no_sales(sales_repo_mock):
    from_date = datetime.now()
    to_date = datetime.now()

    sales_repo_mock.find_from_to_date.return_value = {}

    report = create_sales_report(from_date, to_date, sales_repo_mock)

    assert (
        report
        == f"""
Product            Date        Sales person    Price     Quantity  Total
-------            ----        ------------    -------   --------  ------------

-------------------------------------------------------------------------------
Total:                                                             €    0.00
    """.strip()
    )


def test_one_sale(sales_repo_mock):
    from_date = datetime.now()
    to_date = datetime.now()

    sale: Sale = SaleFactory()
    sales_repo_mock.find_from_to_date.return_value = {sale}

    report = create_sales_report(from_date, to_date, sales_repo_mock)

    product_name = sale.product.name[:18].ljust(18)
    sale_date = str(sale.time_of_sale).ljust(11)
    sold_by = sale.sold_by.name[:15].ljust(15)
    price = "€ " + "{:.2f}".format(sale.product.price).ljust(7)
    quantity = str(sale.quantity).ljust(9)
    sale_total = "€ " + "{:.2f}".format(sale.total).rjust(7)

    expected = f"""
Product            Date        Sales person    Price     Quantity  Total
-------            ----        ------------    -------   --------  ------------
{product_name} {sale_date} {sold_by} {price} {quantity} {sale_total}

-------------------------------------------------------------------------------
Total:                                                             {sale_total}
    """.strip()

    assert (
        report
        == expected
    )


def test_multiple_sales_with_multiple_different_products(sales_repo_mock):
    from_date = datetime.now()
    to_date = datetime.now()

    sale_1: Sale = SaleFactory(product__name="product_1")
    sale_2: Sale = SaleFactory(product__name="product_2")
    sales_repo_mock.find_from_to_date.return_value = {sale_1, sale_2}

    report = create_sales_report(from_date, to_date, sales_repo_mock)

    report_lines = report.splitlines()

    product_names = sorted([sale_1.product.name, sale_2.product.name])

    assert report_lines[2].startswith(product_names[0])
    assert report_lines[3].startswith(product_names[1])


def test_multiple_sales_with_multiple_same_products(sales_repo_mock):
    from_date = datetime.now()
    to_date = datetime.now()

    sale_1: Sale = SaleFactory(product__name="product_1")
    sale_2: Sale = SaleFactory(product__name="product_1")
    sale_3: Sale = SaleFactory(product__name="product_2")
    sales_repo_mock.find_from_to_date.return_value = {sale_1, sale_2, sale_3}

    report = create_sales_report(from_date, to_date, sales_repo_mock)

    report_lines = report.splitlines()

    with (Path() / "report.txt").open("w+") as report_file:
        report_file.write(report)

    assert report_lines[2].startswith("product_1")
    assert report_lines[3].startswith("     ")
    assert report_lines[4].startswith("product_2")

