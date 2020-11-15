from datetime import datetime
from pathlib import Path

import pytest

from python_solid_principles.jas.formatting import format_amount, format_string
from python_solid_principles.jas.sales.entities import Sale
from python_solid_principles.jas.sales.reports import (
    ReportField,
    create_item_line,
    create_item_lines,
    create_report_header,
    create_sales_report_for_ceo,
    create_sales_report_for_sales_manager,
    create_totals_line,
)
from tests.jas.factories import EmployeeFactory, SaleFactory


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


