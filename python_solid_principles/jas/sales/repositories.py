import csv
from datetime import date
from typing import Set

from python_solid_principles.jas.sales.entities import InternalSale, Sale


class SalesRepository:
    def find_from_to_date(self, from_date: date, to_date: date) -> Set[Sale]:
        """Find all sales starting at from_date until to_date"""
        ...

    def add(self, sale: Sale) -> None:
        with open("sales.csv", "w+") as sales_file:
            writer = csv.writer(sales_file)
            is_internal = True if isinstance(sale, InternalSale) else Fale
            writer.writerow(
                [
                    sale.id,
                    sale.product.id,
                    sale.quantity,
                    sale.time_of_sale,
                    sale.sold_by_name,
                    sale.sold_by_manager_name,
                    is_internal,
                ]
            )
