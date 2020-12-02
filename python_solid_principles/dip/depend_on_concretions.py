from typing import Protocol


class Storage(Protocol):
    ...


class SqlStorage(Storage):
    ...


class FileStorage(Storage):
    ...


def storage_factory() -> Storage:
    if config.storage_type == "sql":
        return SqlStorage()
    elif config.storage_type == "file":
        return FileStorage()


class Service:
    def __init__(self, storage: Storage) -> None:
        self.__storage = storage


if __name__ == "__main__":
    a = A()
    b = B()
    c = C(a)
    d = D(b)
    e = E(c, d)
