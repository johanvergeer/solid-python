from datetime import datetime
from pathlib import Path

import pytest

from python_solid_principles.jas.formatting import format_amount, format_string
from python_solid_principles.jas.sales.entities import Sale
from python_solid_principles.jas.sales.reports import (
    create_sales_report,
    ReportField,
    create_report_header,
    create_item_line,
    create_totals_line,
    create_item_lines, create_sales_report_for_sales_manager,
    create_sales_report_for_ceo,
)
from python_solid_principles.jas.sales.repositories import (
    SalesRepository,
)
from tests.jas.factories import SaleFactory, EmployeeFactory


class TestCreateSalesReport:
    @pytest.fixture
    def sales_repo_mock(self, mocker):
        return mocker.MagicMock(name="repo_mock", spec=SalesRepository)

    def test_no_sales(self, sales_repo_mock):
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

    def test_one_sale(self, sales_repo_mock):
        from_date = datetime.now()
        to_date = datetime.now()

        sale: Sale = SaleFactory()
        sales_repo_mock.find_from_to_date.return_value = {sale}

        report = create_sales_report(from_date, to_date, sales_repo_mock)

        product_name = sale.product.name[:18].ljust(18)
        sale_date = str(sale.time_of_sale).ljust(11)
        sold_by = sale.sold_by.name[:15].ljust(15)
        price = "€ " + "{:.2f}".format(sale.product.price).rjust(7)
        quantity = str(sale.quantity).ljust(9)
        sale_total = "€ " + "{:.2f}".format(sale.total).rjust(7)

        expected = f"""
Product            Date        Sales person    Price     Quantity  Total
-------            ----        ------------    -------   --------  ------------
{product_name} {sale_date} {sold_by} {price} {quantity} {sale_total}

-------------------------------------------------------------------------------
Total:                                                             {sale_total}
        """.strip()

        assert report == expected

    def test_multiple_sales_with_multiple_different_products(self, sales_repo_mock):
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

    def test_multiple_sales_with_multiple_same_products(self, sales_repo_mock):
        from_date = datetime.now()
        to_date = datetime.now()

        sale_1: Sale = SaleFactory(product__name="product_1")
        sale_2: Sale = SaleFactory(product__name="product_1")
        sale_3: Sale = SaleFactory(product__name="product_2")
        sales_repo_mock.find_from_to_date.return_value = {sale_1, sale_2, sale_3}

        report = create_sales_report(from_date, to_date, sales_repo_mock)

        report_lines = report.splitlines()

        assert report_lines[2].startswith("product_1")
        assert report_lines[3].startswith("     ")
        assert report_lines[4].startswith("product_2")

    def _format_sale_line_for_ceo(
        self, sale: Sale, include_manager: bool = True
    ) -> str:
        if include_manager:
            sales_manager = sale.sold_by.manager.name.ljust(18)
        else:
            sales_manager = "".ljust(18)
        sale_date = str(sale.time_of_sale).ljust(11)
        product_name = sale.product.name[:18].ljust(18)
        price = "€ " + "{:.2f}".format(sale.product.price).rjust(7)
        quantity = str(sale.quantity).ljust(9)
        sale_total = "€ " + "{:.2f}".format(sale.total).rjust(7)

        return f"{sales_manager} {sale_date} {product_name} {price} {quantity} {sale_total}"

    def test_multiple_sales__multiple_sales_managers__for_ceo(self, sales_repo_mock):
        from_date = datetime.now()
        to_date = datetime.now()
        manager_1 = EmployeeFactory(name="manager_1")
        manager_2 = EmployeeFactory(name="manager_2")

        sale_1: Sale = SaleFactory(
            product__name="product_1", sold_by__manager=manager_1
        )
        sale_2: Sale = SaleFactory(
            product__name="product_1", sold_by__manager=manager_2
        )
        sale_3: Sale = SaleFactory(
            product__name="product_2", sold_by__manager=manager_1
        )
        sales = {sale_1, sale_2, sale_3}
        sales_repo_mock.find_from_to_date.return_value = sales

        report = create_sales_report(from_date, to_date, sales_repo_mock, "ceo")

        sales_total = "€ " + "{:.2f}".format(sum([s.total for s in sales])).rjust(7)

        expected = f"""
Sales Manager      Date        Product            Price     Quantity  Total
-------------      ----        -------            -------   --------  ------------
{self._format_sale_line_for_ceo(sale_1, include_manager=True)}
{self._format_sale_line_for_ceo(sale_3, include_manager=False)}
{self._format_sale_line_for_ceo(sale_2, include_manager=True)}

----------------------------------------------------------------------------------
Total:                                                                {sales_total}
        """.strip()

        assert report == expected

    def test_multiple_sales__for_ceo__skip_sales_below_threshold(self, sales_repo_mock):
        from_date = datetime.now()
        to_date = datetime.now()
        manager_1 = EmployeeFactory(name="manager_1")
        manager_2 = EmployeeFactory(name="manager_2")

        sale_1: Sale = SaleFactory(
            product__name="product_1",
            product__price=100,
            sold_by__manager=manager_1,
            quantity=2,
        )  # Total sale price is 200, so this sale should be included in the report
        sale_2: Sale = SaleFactory(
            product__name="product_2",
            product__price=10,
            sold_by__manager=manager_2,
            quantity=10,
        )  # Total sale price is 100, so this sale should not be included in the report
        sale_3: Sale = SaleFactory(
            product__name="product_3",
            product__price=100,
            sold_by__manager=manager_1,
            quantity=3,
        )  # Total sale price is 300, so this sale should be included in the report
        sales = {sale_1, sale_2, sale_3}
        sales_repo_mock.find_from_to_date.return_value = sales

        report = create_sales_report(
            from_date, to_date, sales_repo_mock, "ceo", minimum_sale_threshold=200
        )

        sales_total = "€ " + "{:.2f}".format(sum([sale_1.total, sale_3.total])).rjust(7)

        expected = f"""
Sales Manager      Date        Product            Price     Quantity  Total
-------------      ----        -------            -------   --------  ------------
{self._format_sale_line_for_ceo(sale_1, include_manager=True)}
{self._format_sale_line_for_ceo(sale_3, include_manager=False)}

----------------------------------------------------------------------------------
Total:                                                                {sales_total}
        """.strip()

        with (Path() / "report.txt").open("w+") as report_file:
            report_file.write(report)

        assert report == expected


class TestCreateReportHeader:
    def test_single_field(self):
        field = ReportField("na", "Field 1", 10)
        header = create_report_header([field])

        expected = "Field 1   "

        assert header == expected

    def test_multiple_fields(self):
        field_1 = ReportField("na", "Field 1", 10)
        field_2 = ReportField("na", "Field 2", 8)
        header = create_report_header([field_1, field_2])

        expected = "Field 1    Field 2 "

        assert header == expected


class TestCreateItemLine:
    def test_single_field(self):
        sale = SaleFactory()
        field = ReportField("total", "Total", 10, format_amount)

        expected = format_amount(sale.total, 10)

        report_line = create_item_line([field], sale)

        assert report_line == expected

    def test_multiple_fields(self):
        sale = SaleFactory()

        field_1 = ReportField("total", "Total", 10, format_amount)
        field_2 = ReportField("sold_by__name", "Sales person", 16, format_string)

        expected = (
            format_amount(sale.total, 10) + " " + format_string(sale.sold_by.name, 16)
        )

        report_line = create_item_line([field_1, field_2], sale)

        assert report_line == expected

    def test_multiple_fields__skip_one_field(self):
        sale = SaleFactory()

        field_1 = ReportField("product__name", "Product name", 19, format_string)
        field_2 = ReportField("sold_by__name", "Sales person", 16, format_string)
        field_3 = ReportField("total", "Total", 10, format_amount)

        expected = (
            " " * field_1.length
            + " "
            + format_string(sale.sold_by.name, 16)
            + " "
            + format_amount(sale.total, 10)
        )

        report_line = create_item_line(
            [field_1, field_2, field_3], sale, fields_to_skip=["product__name"]
        )

        assert report_line == expected


class TestCreateTotalsLine:
    def test_two_fields__single_sale(self):
        sale = SaleFactory()
        field_1 = ReportField("product__name", "Product name", 19, format_string)
        field_2 = ReportField("total", "Total", 10, format_amount)

        expected = format_string("Total:", 19) + " " + format_amount(sale.total, 10)

        report_line = create_totals_line([field_1, field_2], [sale], "total")

        assert report_line == expected

    def test_two_fields__multiple_sales(self):
        sale_1 = SaleFactory()
        sale_2 = SaleFactory()

        field_1 = ReportField("product__name", "Product name", 19, format_string)
        field_2 = ReportField("total", "Total", 10, format_amount)

        expected = (
            format_string("Total:", 19)
            + " "
            + format_amount(sale_1.total + sale_2.total, 10)
        )

        report_line = create_totals_line([field_1, field_2], [sale_1, sale_2], "total")

        assert report_line == expected

    def test_sales_total_not_last_field(self):
        sale = SaleFactory()
        field_1 = ReportField("product__name", "Product name", 19, format_string)
        field_2 = ReportField("total", "Total", 10, format_amount)
        field_3 = ReportField("sold_by__name", "Sales person", 19, format_string)

        expected = (
            format_string("Total:", 19)
            + " "
            + format_amount(sale.total, 10)
            + " " * field_3.length
            + " "
        )

        report_line = create_totals_line([field_1, field_2, field_3], [sale], "total")

        assert report_line == expected


class TestCreateItemLines:
    @pytest.fixture
    def fields(self):
        field_1 = ReportField("product__name", "Product name", 19, format_string)
        field_2 = ReportField("total", "Total", 10, format_amount)
        field_3 = ReportField("sold_by__name", "Sales person", 19, format_string)

        return [field_1, field_2, field_3]

    def test_no_item_lines(self, fields):
        assert create_item_lines(fields, []) == ""

    def test_single_item_line(self, fields):
        sale = SaleFactory()

        expected = create_item_line(fields, sale)

        assert create_item_lines(fields, [sale]) == expected

    def test_multiple_item_lines__ungrouped(self, fields):
        sale_1 = SaleFactory()
        sale_2 = SaleFactory()

        expected = (
            create_item_line(fields, sale_1) + "\n" + create_item_line(fields, sale_2)
        )

        assert create_item_lines(fields, [sale_1, sale_2]) == expected


def test_create_sales_report_for_sales_manager():
    sale_1 = SaleFactory()
    sale_2 = SaleFactory()

    with (Path() / "report.txt").open("w+") as report_file:
        report_file.write(create_sales_report_for_sales_manager([sale_1, sale_2]))


def test_create_sales_report_for_ceo():
    manager_1 = EmployeeFactory(name="manager_1")
    manager_2 = EmployeeFactory(name="manager_2")

    sale_1: Sale = SaleFactory(
        product__name="product_1", sold_by__manager=manager_1
    )
    sale_2: Sale = SaleFactory(
        product__name="product_1", sold_by__manager=manager_2
    )
    sale_3: Sale = SaleFactory(
        product__name="product_2", sold_by__manager=manager_1
    )

    with (Path() / "report.txt").open("w+") as report_file:
        report_file.write(create_sales_report_for_ceo([sale_1, sale_2, sale_3]))


