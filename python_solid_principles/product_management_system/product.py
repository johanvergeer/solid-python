import logging
import sqlite3
from enum import Enum
from sqlite3 import Connection

logger = logging.getLogger(__name__)


class Product:
    def __init__(self, id_: int, name: str, country_of_origin: str, price: float):
        self.__id = id_
        self.name = name
        self.country_of_origin = country_of_origin
        self.price = price

    @property
    def id(self):
        return self.__id


class DrinkType(Enum):
    DISTILLED = "distilled"
    WINE = "wine"
    BEER = "beer"


class Drink(Product):
    def __init__(
        self,
        id_: int,
        name: str,
        country_of_origin: str,
        price: float,
        type_: DrinkType,
        alcohol_percentage: float,
    ):
        super(Drink, self).__init__(id_, name, country_of_origin, price)
        self.type = type_
        self.alcohol_percentage = alcohol_percentage


class ElectronicProductType(Enum):
    E_READER = "e_reader"
    EXTERNAL_HDD = "external_harddisk"
    SMARTPHONE = "smartphone"
    TABLET = "tablet"
    PC = "pc"


class ElectronicProduct(Product):
    def __init__(
        self,
        id_: int,
        name: str,
        country_of_origin: str,
        price: float,
        type_: ElectronicProductType,
    ):
        super(ElectronicProduct, self).__init__(id_, name, country_of_origin, price)
        self.type = type_


def calculate_total_taxes(product: Product) -> float:
    if isinstance(product, Drink):
        if product.type == DrinkType.BEER:
            if product.alcohol_percentage > 0.5:
                vat = product.price * 0.21
            else:
                vat = product.price * 0.09
        elif product.type == DrinkType.DISTILLED:
            vat = product.price * 0.21
        elif product.type == DrinkType.WINE:
            if product.alcohol_percentage > 1.2:
                vat = product.price * 0.21
            else:
                vat = product.price * 0.09
        else:
            raise ValueError(f"Cannot calculate vat for {product.type.value}")

        return vat

    elif isinstance(product, ElectronicProduct):
        vat = product.price * 0.21

        if product.type == ElectronicProductType.E_READER:
            home_copy_tax = 0.8
        elif product.type == ElectronicProductType.EXTERNAL_HDD:
            home_copy_tax = 0.6
        elif product.type == ElectronicProductType.SMARTPHONE:
            home_copy_tax = 4.7
        elif product.type == ElectronicProductType.TABLET:
            home_copy_tax = 2.6
        elif product.type == ElectronicProductType.PC:
            home_copy_tax = 2.6
        else:
            raise ValueError(
                f"Cannot calculate home copy tax for a {product.type.value}"
            )

        return vat + home_copy_tax

    raise ValueError("Unable to calculate tax for product.")


class ProductRepository:
    def __init__(self, connection: Connection):
        self.connection = connection

    def exists(self, product: Product) -> bool:
        """Returns True if a product with the same id exists, else False."""
        cur = self.connection.cursor()
        cur.execute("SELECT EXISTS(SELECT 1 FROM products WHERE id=?)", (product.id,))

        return bool(cur.fetchone()[0])

    def add(self, product: Product) -> None:
        """Adds a new product to the database

        Raises:
             sqlite3.IntegrityError: when a product with the same id already exists
        """
        cur = self.connection.cursor()
        insert_sql = """INSERT INTO products(id, name, country_of_origin)
                        VALUES (?,?,?)"""
        cur.execute(insert_sql, (product.id, product.name, product.country_of_origin))

    def update(self, product: Product) -> None:
        """Updates a product in the database with the given id

        Warnings:
            - No error is raised when no product with the given id
            already exists in the database.
        """
        cur = self.connection.cursor()
        update_sql = """UPDATE products
                        SET name=?, country_of_origin=?
                        WHERE id=?"""
        cur.execute(update_sql, (product.name, product.country_of_origin, product.id))

    def add_or_update(self, product: Product) -> None:
        """Adds the product to the database if no product with the
        same id already exists, else the product will be updated.
        """
        if self.exists(product):
            logger.info(f"Product with id {product.id} found in database. Updating...")
            self.update(product)
        else:
            logger.info(f"Adding new product with id {product.id} to database")
            self.add(product)


"""
1. Extract save method to ProductRepository
2. Move conn to ProductRepository init
3. Extract method to check whether product exists
4. Extract add method
5. Extract update method
6. Rename 'save' to 'add_or_update'

When add is called and the product already exists in the database,
an exception is raised. Same for update, but the other way around
"""

if __name__ == "__main__":
    p = Product(1, "friet", "NL")
    connection = sqlite3.connect("products.db")
    pr = ProductRepository(connection)

    pr.update(p)
    pr.add(Product(10, "foo", "NL"))

    connection.commit()

    connection.close()
