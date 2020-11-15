class Rectangle:
    def __init__(self, width: float, height: float):
        self.width = width
        self.height = height

    @property
    def area(self) -> float:
        return self.width * self.height

    @property
    def perimiter(self) -> float:
        return self.width * 2 + self.height * 2


class Square:
    def __init__(self, side: float):
        self.side = side

    @property
    def area(self):
        return self.side ** 2

    @property
    def perimiter(self):
        return self.side * 4
