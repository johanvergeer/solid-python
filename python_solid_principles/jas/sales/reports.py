from datetime import date
from itertools import groupby
from typing import Literal, Optional

from python_solid_principles.jas.formatting import format_amount
from python_solid_principles.jas.sales.repositories import (
    SalesRepository,
)


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
