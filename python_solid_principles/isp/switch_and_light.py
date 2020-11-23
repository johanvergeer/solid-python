class Light:
    def switch_on(self) -> None:
        print("Switching the light on.")

    def switch_off(self) -> None:
        print("Switching the light off.")

    def dim(self, amount: int) -> None:
        raise NotImplemented("This light doesn't dim")


class Switch:
    def __init__(self, light: Light) -> None:
        self.__light = light

    def switch_on(self) -> None:
        self.__light.switch_on()

    def switch_off(self) -> None:
        self.__light.switch_off()

    def dim(self, amount: int) -> None:
        self.__light.dim(amount)
