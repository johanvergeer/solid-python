from typing import Protocol


class Switchable(Protocol):
    def switch_on(self) -> None:
        ...

    def switch_off(self) -> None:
        ...

    def dim(self) -> None:
        ...


class Light(Switchable):
    def __init__(self) -> None:
        self.__state = "enabled"

    def switch_on(self) -> None:
        self.__state = "enabled"

    def switch_off(self) -> None:
        self.__state = "disabled"

    def dim(self) -> None:
        raise NotImplementedError("This light doesn't dim!")
