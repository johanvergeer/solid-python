from typing import Optional


class Employee:
    def __init__(self, id_: int, name: str, manager: Optional["Employee"]) -> None:
        self.__id = id_
        self.__name = name
        self.__manager = manager

    @property
    def id(self):
        return self.__id

    @property
    def name(self):
        return self.__name

    @property
    def manager(self):
        return self.__manager


class Reseller(Employee):
    def __init__(self, id_: int, name: str, contact: Employee) -> None:
        super(Reseller, self).__init__(id_, name, None)
        self.contact = contact
