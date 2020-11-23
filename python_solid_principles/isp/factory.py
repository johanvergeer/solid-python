from datetime import date
from typing import List


class Invoice:
    pass


class Storage:
    def find_invoices(self, start_date: date, end_date: date) -> List[Invoice]:
        ...


class StorageFactory:
    def create(self) -> Storage:
        return Storage()


class Report:
    pass


class ReportGenerator:
    def __init__(self) -> None:
        self.__storage_factory = StorageFactory()

    def create_invoice_report(self, start_date: date, end_date: date) -> Report:
        storage = self.__storage_factory.create()
        invoices = storage.find_invoices(start_date, end_date)

        # Create report


class ReportGenerator:
    def __init__(self, storage: Storage) -> None:
        self.__storage = storage

    def create_invoice_report(self, start_date: date, end_date: date) -> Report:
        invoices = self.__storage.find_invoices(start_date, end_date)

        # Create report

