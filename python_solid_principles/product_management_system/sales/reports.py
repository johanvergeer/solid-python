from datetime import date
from itertools import groupby

from python_solid_principles.product_management_system.sales.repositories import (
    SalesRepository,
)


def create_sales_report(
    from_date: date, to_date: date, sales_repository: SalesRepository
):
    sales = sales_repository.find_from_to_date(from_date, to_date)
    sales = sorted(sales, key=lambda s: s.product.name)

    sales_total = "€ " + "{:.2f}".format(sum([s.total for s in sales])).rjust(7)

    sales_by_product = groupby(sales, key=lambda s: s.product.name)


    report = """
Product            Date        Sales person    Price     Quantity  Total
-------            ----        ------------    -------   --------  ------------"""

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

    report += f"""

-------------------------------------------------------------------------------
Total:                                                             {sales_total}
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
