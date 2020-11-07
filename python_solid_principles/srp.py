import logging
import smtplib
import ssl
from pathlib import Path
from typing import List

logger = logging.getLogger(__name__)


def send_file_to_email(file_name: str) -> List[str]:
    logger.info(f"Trying to read file: '{file_name}'")

    with open(Path() / file_name) as f:
        lines = f.readlines()

    context = ssl.create_default_context()

    password = input("Type your password: ")
    sender_email = "my@gmail.com"
    receiver_email = "your@gmail.com"
    port = 465

    message = "\n".join(lines)

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login("me@gmail.com", password)
        server.sendmail(sender_email, receiver_email, message)

    logger.info(f"Email sent: '{file_name}'")

    return lines


class Main:
    def open(self, name: str):
        ...

    def close(self):
        ...

    def log(self):
        ...

    def save(self):
        ...

    def print(self):
        ...

    def send_email(self):
        ...


def calculate_price(product):
    if product.on_sale:
        ...
    elif product.for_free:
        ...
    else:
        ...


def calculate_price(
    product_name: str,
    price: float,
    on_sale: bool,
    for_free: bool,
    calculation_method: str,
    country_of_origin: str,
    related_product_ids: str,
) -> float:
    ...


class Report:
    pass


class Sale:
    pass


def generate_sales_report(sales: List[Sale]) -> Report:
    ...
