from abc import ABC, abstractmethod


class Duck(ABC):
    @abstractmethod
    def quack(self):
        ...

    @abstractmethod
    def walk(self):
        ...

    @abstractmethod
    def fly(self):
        ...

    @abstractmethod
    def land(self):
        ...


class Mallard(Duck):
    def quack(self):
        print("Quacking")

    def walk(self):
        print("Walking")

    def fly(self):
        print("Flying")

    def land(self):
        print("Landing")


class NoFlyException(Exception):
    pass


class RubberDuck(Duck):
    def quack(self):
        print("Squeek")

    def walk(self):
        pass

    def fly(self):
        raise NoFlyException()

    def land(self):
        raise NoFlyException()


class RoboDuck(Duck):
    def __init__(self):
        self.height = 0

    def quack(self):
        print("목쉰 소리")  # Made in Korea

    def walk(self):
        print("Walking")

    def fly(self):
        if self.height > 500:
            self.land()
        self.height += 1

    def land(self):
        self.height = 0
