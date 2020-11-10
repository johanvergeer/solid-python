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


def create_sales_report(
    from_date: date,
    to_date: date,
    sales_repository: SalesRepository,
    requested_by: Literal["sales_manager, ceo"] = "sales_manager",
    minimum_sale_threshold: Optional[int] = None,
):
    # Find all sales that occurred from 'from_date' until 'to_date'
    sales = sales_repository.find_from_to_date(from_date, to_date)

    # The CEO is only interested in sales where the total amount
    # is above a certain threshold.
    if requested_by == "ceo" and minimum_sale_threshold is not None:
        sales = [s for s in sales if s.total >= minimum_sale_threshold]

    # Get the sales total for all sales
    sales_total = format_amount(sum([s.total for s in sales]))

    # Initialize the 'report' string
    report = ""

    # Add the report header
    if requested_by == "sales_manager":
        # The sales manager needs the sales grouped by product,
        # including the date, sales person, product price,quantity and total amount
        report = """
Product            Date        Sales person    Price     Quantity  Total
-------            ----        ------------    -------   --------  ------------"""
    elif requested_by == "ceo":
        # The CEO wants to know which sales manager the sales person reports to,
        # the date, product, product price, quantity and total amount.
        report = f"""
Sales Manager      Date        Product            Price     Quantity  Total
-------------      ----        -------            -------   --------  ------------"""

    if requested_by == "sales_manager":
        # The sales manager wants all sales to be grouped by the product
        sales = sorted(sales, key=lambda s: s.product.name)
        sales_by_product = groupby(sales, key=lambda s: s.product.name)

        for product_name, sales_for_product in sales_by_product:
            for sale_nr, sale in enumerate(sales_for_product):
                # Only add the product name on the report for the first sale
                # of that product
                if sale_nr == 0:
                    product_name = product_name[:18].ljust(18)
                else:
                    product_name = "".ljust(18)

                # Format values
                sale_date = str(sale.time_of_sale).ljust(11)
                sold_by = sale.sold_by.name[:15].ljust(15)
                price = format_amount(sale.product.price)
                quantity = str(sale.quantity).ljust(9)
                sale_total = format_amount(sale.total)

                # Add the sale to the report
                report += f"\n{product_name} {sale_date} {sold_by} {price} {quantity} {sale_total}"
    elif requested_by == "ceo":
        # The ceo wants all sales to be grouped by the manager
        sales = sorted(sales, key=lambda s: (s.sold_by.manager.name, s.product.name))
        sales_by_manager = groupby(sales, key=lambda s: s.sold_by.manager.name)

        for sales_manager_name, sales_for_manager in sales_by_manager:
            for sale_nr, sale in enumerate(sales_for_manager):
                # Only add the sales manager name on the report for the first sale
                # of that manager
                sales_manager_name = (
                    sales_manager_name[:18].ljust(18) if sale_nr == 0 else "".ljust(18)
                )

                # Format values
                sale_date = str(sale.time_of_sale).ljust(11)
                product_name = sale.product.name.ljust(18)
                price = format_amount(sale.product.price)
                quantity = str(sale.quantity).ljust(9)
                sale_total = format_amount(sale.total)

                # Add the sale to the report
                report += f"\n{sales_manager_name} {sale_date} {product_name} {price} {quantity} {sale_total}"

    # Add totals
    if requested_by == "sales_manager":
        report += f"""

-------------------------------------------------------------------------------
Total:                                                             {sales_total}
"""

    elif requested_by == "ceo":
        report += f"""

----------------------------------------------------------------------------------
Total:                                                                {sales_total}
"""

    return report.strip()


"""
Sales manager report:
- list of all sales including sales person, date, product, quantity
- grouped by product

CEO report:
- list of all sales including, date, product, quantity
- grouped by sales manager
- only include sales that are above a certain amount
"""
