from datetime import date
from itertools import groupby
from typing import Literal, Optional

from python_solid_principles.product_management_system.sales.repositories import (
    SalesRepository,
)


def create_sales_report(
    from_date: date,
    to_date: date,
    sales_repository: SalesRepository,
    requested_by: Literal["sales_manager, ceo"] = "sales_manager",
):
    sales = sales_repository.find_from_to_date(from_date, to_date)
    sales_total = "€ " + "{:.2f}".format(sum([s.total for s in sales])).rjust(7)

    report = ""
    if requested_by == "sales_manager":
        report = """
Product            Date        Sales person    Price     Quantity  Total
-------            ----        ------------    -------   --------  ------------"""
    elif requested_by == "ceo":
        report = f"""
Sales Manager      Date        Product            Price     Quantity  Total
-------------      ----        -------            -------   --------  ------------"""

    if requested_by == "sales_manager":
        sales = sorted(sales, key=lambda s: s.product.name)
        sales_by_product = groupby(sales, key=lambda s: s.product.name)

        for product_name, sales_for_product in sales_by_product:
            for sale_nr, sale in enumerate(sales_for_product):
                if sale_nr == 0:
                    product_name = product_name[:18].ljust(18)
                else:
                    product_name = "".ljust(18)

                sale_date = str(sale.time_of_sale).ljust(11)
                sold_by = sale.sold_by.name[:15].ljust(15)
                price = "€ " + "{:.2f}".format(sale.product.price).ljust(7)
                quantity = str(sale.quantity).ljust(9)
                sale_total = "€ " + "{:.2f}".format(sale.total).rjust(7)

                report += f"\n{product_name} {sale_date} {sold_by} {price} {quantity} {sale_total}"
    elif requested_by == "ceo":
        sales = sorted(sales, key=lambda s: (s.sold_by.manager.name, s.product.name))
        sales_by_manager = groupby(sales, key=lambda s: s.sold_by.manager.name)

        for sales_manager_name, sales_for_manager in sales_by_manager:
            for sale_nr, sale in enumerate(sales_for_manager):
                sales_manager_name = (
                    sales_manager_name[:18].ljust(18) if sale_nr == 0 else "".ljust(18)
                )

                sale_date = str(sale.time_of_sale).ljust(11)
                product_name = sale.product.name.ljust(18)
                price = "€ " + "{:.2f}".format(sale.product.price).ljust(7)
                quantity = str(sale.quantity).ljust(9)
                sale_total = "€ " + "{:.2f}".format(sale.total).rjust(7)

                report += f"\n{sales_manager_name} {sale_date} {product_name} {price} {quantity} {sale_total}"

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
