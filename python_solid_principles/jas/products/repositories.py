import logging
from sqlite3 import Connection

from python_solid_principles.jas.products.entities import Product

logger = logging.getLogger(__name__)


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
        insert_sql = """INSERT INTO products(id, name, country_of_origin, price)
                        VALUES (?,?,?, ?)"""
        cur.execute(
            insert_sql,
            (product.id, product.name, product.country_of_origin, product.price),
        )

    def update(self, product: Product) -> None:
        """Updates a product in the database with the given id

        Warnings:
            - No error is raised when no product with the given id
            already exists in the database.
        """
        cur = self.connection.cursor()
        update_sql = """UPDATE products
                        SET name=?, country_of_origin=?, price=?
                        WHERE id=?"""
        cur.execute(
            update_sql,
            (product.name, product.country_of_origin, product.id, product.price),
        )

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
