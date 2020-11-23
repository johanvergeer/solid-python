from typing import Protocol


class StateAwareSwitch(Protocol):
    def on_switched_on(self) -> None:
        ...

    def on_switched_off(self) -> None:
        ...


class Switchable(Protocol):
    def switch_on(self) -> None:
        ...

    def switch_off(self) -> None:
        ...


class Dimmable(Protocol):
    def dim(self, amount: int) -> None:
        ...


class Light(Switchable, Dimmable):
    def __init__(self):
        self.__intensity = 100

    def switch_on(self) -> None:
        self.__intensity = 100

    def switch_off(self) -> None:
        self.__intensity = 0

    def dim(self, amount: int) -> None:
        if self.__intensity + amount > 100:
            self.__intensity = 100
        elif self.__intensity + amount < 0:
            self.__intensity = 0
        else:
            self.__intensity += amount


class Switch:
    def __init__(self, switchable: Switchable, dimmable: Dimmable) -> None:
        self.__switchable = switchable
        self.__dimmable = dimmable

    def switch_on(self) -> None:
        self.__switchable.switch_on()

    def switch_off(self) -> None:
        self.__switchable.switch_off()

    def dim(self, amount: int) -> None:
        self.__dimmable.dim(amount)


class Button(StateAwareSwitch):
    def __init__(self, switchable: Switchable) -> None:
        self.__switchable = switchable

        self.__switched_on = False

    def press(self):
        if self.__switched_on:
            self.__switchable.switch_off()
        else:
            self.__switchable.switch_on()

    def on_switched_on(self) -> None:
        self.__switched_on = True

    def on_switched_off(self) -> None:
        self.__switched_on = False


class Relay(Switchable):
    def __init__(self, switch: StateAwareSwitch, switchable: Switchable) -> None:
        self.__switch = switch
        self.__switchable = switchable

    def switch_on(self) -> None:
        self.__switchable.switch_on()
        self.__switch.on_switched_on()

    def switch_off(self) -> None:
        self.__switchable.switch_off()
        self.__switch.on_switched_off()
