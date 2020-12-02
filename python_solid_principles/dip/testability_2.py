from dataclasses import dataclass
from datetime import date
from typing import List
from unittest.mock import ANY, create_autospec


class Invoice:
    ...


@dataclass
class Report:
    ...


class Storage:
    def find_invoices(self, start_date: date, end_date: date) -> List[Invoice]:
        ...


def generate_report(storage: Storage, start_date: date, end_date: date) -> Report:
    invoices = storage.find_invoices(start_date, end_date)
    ...  # Doing some interesting stuff
    return Report()


def test_generate_report() -> None:
    storage_mock = create_autospec(Storage)
    storage_mock.find_invoices.return_value = [Invoice()]

    report = generate_report(storage_mock, ANY, ANY)

    assert report == Report()
    storage_mock.find_invoices.assert_called_once_with(ANY, ANY)
