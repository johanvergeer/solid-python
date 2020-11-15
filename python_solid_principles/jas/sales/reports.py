from datetime import date
from itertools import groupby
from typing import Literal, Optional, Callable, List, Tuple, Union

from python_solid_principles.jas.formatting import (
    format_amount,
    format_string,
    format_date,
    format_any,
)
from python_solid_principles.jas.sales.entities import Sale
from python_solid_principles.jas.sales.repositories import (
    SalesRepository,
)


class ReportField:
    def __init__(
        self,
        path: str,
        title: str,
        length: int,
        formatter: Optional[Callable] = None,
        **formatter_options,
    ):
        self.path = path
        self.title = title
        self.length = length
        self.formatter = formatter
        self.formatter_options = formatter_options


def create_horizontal_line(fields: List[ReportField]) -> str:
    horizontal_line = ""
    for field in fields:
        horizontal_line += "-" * (field.length + 1)
    return horizontal_line[:-1]


def create_report_header(fields: List[ReportField]) -> str:
    header = ""
    for field in fields:
        header += field.title.ljust(field.length + 1)
    header = header[:-1]

    return header


def get_attribute_value_from_path(sale: Sale, path: str):
    value = sale
    for attribute in path.split("__"):
        value = getattr(value, attribute)
    return value


def create_item_line(
    fields: List[ReportField], sale: Sale, fields_to_skip: Optional[List[str]] = None
) -> str:
    fields_to_skip = fields_to_skip or []

    report_line = ""
    for field in fields:
        if field.path in fields_to_skip:
            report_line += " " * field.length + " "
        else:
            formatter = field.formatter or format_any
            value = get_attribute_value_from_path(sale, field.path)
            report_line += (
                formatter(value, field.length, **field.formatter_options) + " "
            )

    return report_line[:-1]


def create_item_lines(
    fields: List[ReportField], sales: List[Sale], group_attr_path: Optional[str] = None
):
    lines = []
    current_group_value = ""
    for sale in sales:
        if group_attr_path:
            # Items should be grouped
            if current_group_value != (
                new_group_value := get_attribute_value_from_path(sale, group_attr_path)
            ):
                lines.append(create_item_line(fields, sale))
                current_group_value = new_group_value
            else:
                lines.append((create_item_line(fields, sale, [group_attr_path])))
        else:
            # Items don't have to be grouped
            lines.append(create_item_line(fields, sale))

    return "\n".join(lines)


def create_totals_line(
    fields: List[ReportField], sales: List[Sale], totals_column: str
) -> str:
    totals_line = format_string("Total: ", fields[0].length) + " "

    for field in fields[1:]:
        if field.path != totals_column:
            totals_line += (" " * field.length) + " "
        else:
            total_amount_value = sum(
                [get_attribute_value_from_path(s, field.path) for s in sales]
            )
            total_amount_formatted = field.formatter(
                total_amount_value, field.length, **field.formatter_options
            )

            totals_line += total_amount_formatted + " "

    return totals_line[:-1]


def create_sales_report_for_sales_manager(sales: List[Sale]) -> str:
    sales = sorted(sales, key=lambda s: s.product.name)

    fields = [
        ReportField("product__name", "Product", 18),
        ReportField("time_of_sale", "Date", 10),
        ReportField("sold_by__name", "Sales Person", 15),
        ReportField("product__price", "Price", 9, formatter=format_amount),
        ReportField("quantity", "Quantity", 9),
        ReportField("total", "Total", 9, formatter=format_amount),
    ]

    report_lines = [
        create_report_header(fields),
        create_horizontal_line(fields),
        create_item_lines(fields, sales, "product__name"),
        create_horizontal_line(fields),
        create_totals_line(fields, sales, "total"),
    ]

    return "\n".join(report_lines)


def create_sales_report_for_ceo(sales: List[Sale]) -> str:
    sales = sorted(sales, key=lambda s: (s.sold_by.manager.name, s.product.name))

    fields = [
        ReportField("sold_by__manager__name", "Sales Manager", 18),
        ReportField("time_of_sale", "Date", 10),
        ReportField("product__name", "Product", 18),
        ReportField("product__price", "Price", 9, formatter=format_amount),
        ReportField("quantity", "Quantity", 9),
        ReportField("total", "Total", 9, formatter=format_amount),
    ]

    report_lines = [
        create_report_header(fields),
        create_horizontal_line(fields),
        create_item_lines(fields, sales, "sold_by__manager__name"),
        create_horizontal_line(fields),
        create_totals_line(fields, sales, "total"),
    ]

    return "\n".join(report_lines)
