from python_solid_principles.jas.employees.entities import Employee


class Reseller:
    def __init__(self, id_: int, name: str, contact: Employee) -> None:
        self.__id = id_
        self.__name = name
        self.contact = contact

    @property
    def id(self) -> int:
        return self.__id

    @property
    def name(self) -> str:
        return self.__name
