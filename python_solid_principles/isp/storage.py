class InvoiceStorage:
    ...


class StockStorage:
    ...


class PurchaseOrderStorage:
    ...


class ManufacturingOrderStorage:
    ...


class EmployeeStorage:
    ...


class Storage(
    InvoiceStorage,
    StockStorage,
    PurchaseOrderStorage,
    ManufacturingOrderStorage,
    EmployeeStorage,
):
    ...


class Invoicing:
    def __init__(self, invoice_storage: InvoiceStorage) -> None:
        self.__invoice_storage = invoice_storage


class Planning:
    def __init__(
        self,
        stock_storage: StockStorage,
        purchase_order_storage: PurchaseOrderStorage,
        manufacturing_order_storage: ManufacturingOrderStorage,
    ) -> None:
        self.__stock_storage = stock_storage
        self.__purchase_order_storage = purchase_order_storage
        self.__manufacturing_order_storage = manufacturing_order_storage


class HR:
    def __init__(self, employee_storage: EmployeeStorage) -> None:
        self.__employee_storage = employee_storage


if __name__ == "__main__":
    storage = Storage()
    planning = Planning(storage, storage, storage)
