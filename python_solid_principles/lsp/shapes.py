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

class Square(Rectangle):
    def __init__(self, side: float):
        self.__side = side
        super(Square, self).__init__(side, side)

    @property
    def width(self):
        return self.__side

    @width.setter
    def width(self, value):
        self.__side = value

    @property
    def height(self):
        return self.__side

    @height.setter
    def height(self, value):
        self.__side = value
