from typing import Any, List


class Mallard:
    def quack(self):
        print("Quacking")

    def walk(self):
        print("Walking")

    def fly(self):
        print("Flying")

    def land(self):
        print("Landing")


class RubberDuck:
    def quack(self):
        print("Squeek")


class RoboDuck:
    def __init__(self):
        self.height = 0

    def quack(self):
        print("목쉰 소리")  # Made in Korea

    def walk(self):
        print("Walking")

    def fly(self):
        if self.height > 120:
            self.land()
        self.height += 1
        print(f"Increased height to {self.height} m")

    def land(self):
        self.height = 0


def fly_all_ducks(ducks: List[Any]) -> None:
    for duck in ducks:
        fly_op = getattr(duck, "fly", None)
        if callable(fly_op):
            fly_op()
