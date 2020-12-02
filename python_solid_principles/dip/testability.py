from dataclasses import dataclass
from datetime import date
from typing import List
from unittest.mock import patch, MagicMock, ANY


class Invoice:
    ...


@dataclass
class Report:
    ...


class SqlStorage:
    def find_invoices(self, start_date: date, end_date: date) -> List[Invoice]:
        ...


def generate_report(start_date: date, end_date: date) -> Report:
    storage = SqlStorage()
    invoices = storage.find_invoices(start_date, end_date)
    ...  # Doing some interesting stuff
    return Report()


@patch("python_solid_principles.dip.testability.SqlStorage", autospec=True)
def test_generate_report(sql_storage_mock: MagicMock) -> None:
    sql_storage_mock.find_invoices.return_value = [Invoice()]

    report = generate_report(ANY, ANY)

    assert report == Report()
