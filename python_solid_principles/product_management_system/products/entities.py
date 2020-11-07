class Product:
    def __init__(
        self, id_: int, name: str, country_of_origin: str, price: float
    ) -> None:
        self.__id = id_
        self.name = name
        self.country_of_origin = country_of_origin
        self.price = price

    @property
    def id(self) -> int:
        return self.__id
