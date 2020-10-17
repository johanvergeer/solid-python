import csv
import logging
import shutil
from pathlib import Path
from typing import Dict, Union

logger = logging.getLogger(__name__)


class Product:
    def __init__(self, id_: int, name: str, country_of_origin: str):
        self.__id = id_
        self.name = name
        self.country_of_origin = country_of_origin

    @property
    def id(self):
        return self.__id

    def as_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "country_of_origin": self.country_of_origin,
        }

    def save(self):
        products_file_path = Path() / "products.csv"
        backup_path = Path() / "products.csv.bak"
        fieldnames = [key for key in self.as_dict()]
        products: Dict[int, Dict[str, Union[str, int]]] = {}

        try:
            with open(products_file_path) as products_file:
                product_reader = csv.DictReader(products_file, fieldnames=fieldnames)
                next(product_reader, None)  # Skip the headers

                products = {int(p["id"]): p for p in product_reader}

            # Create backup of current csv file
            shutil.copy(products_file_path, backup_path)
        except FileNotFoundError:
            logger.info("Products file doesn't exist.")
            logger.info("Creating new products file.")

        # Add or replace product in list
        products[self.id] = self.as_dict()

        with open(products_file_path, "w+") as products_file:
            product_writer = csv.DictWriter(products_file, fieldnames=fieldnames)

            product_writer.writeheader()

            for _, product in products.items():
                product_writer.writerow(product)

        # Remove the backup after saving the file succeeded.
        backup_path.unlink()


if __name__ == '__main__':
    p = Product(3, "hamburger", "NL")
    p.save()
