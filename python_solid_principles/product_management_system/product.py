import logging
import sqlite3

logger = logging.getLogger(__name__)


class Product:
    def __init__(self, id_: int, name: str, country_of_origin: str):
        self.__id = id_
        self.name = name
        self.country_of_origin = country_of_origin

    @property
    def id(self):
        return self.__id

    def save(self):
        conn = sqlite3.connect("products.db")

        cur = conn.cursor()
        cur.execute("SELECT EXISTS(SELECT 1 FROM products WHERE id=?)", (self.id,))

        with conn:
            if cur.fetchone()[0]:
                logger.info(f"Product with id {self.id} found in database. Updating...")
                update_sql = """UPDATE products
                                SET name=?, country_of_origin=?
                                WHERE id=?"""
                cur.execute(update_sql, (self.name, self.country_of_origin, self.id))
            else:
                logger.info(f"Adding new product with id {self.id} to database")
                insert_sql = """INSERT INTO products(id, name, country_of_origin)
                                VALUES (?,?,?)"""
                cur.execute(insert_sql, (self.id, self.name, self.country_of_origin))

        conn.close()


if __name__ == "__main__":
    p = Product(1, "ham", "NL")
    p.save()
