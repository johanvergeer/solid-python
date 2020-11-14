import pytest

from python_solid_principles.lsp.shapes import Rectangle, Square


class TestRectangle:
    @pytest.fixture
    def rectangle(self):
        return Rectangle(12, 15)

    def test_init(self, rectangle):
        assert rectangle.width == 12
        assert rectangle.height == 15

    def test_set_width(self, rectangle):
        rectangle.width = 100
        assert rectangle.width == 100

    def test_set_height(self, rectangle):
        rectangle.height = 100
        assert rectangle.height == 100

    def test_area(self, rectangle):
        assert rectangle.area == 12 * 15

    def test_perimiter(self, rectangle):
        assert rectangle.perimiter == 12 * 2 + 15 * 2


class TestSquare:
    @pytest.fixture
    def square(self):
        return Square(20)

    def test_init(self, square):
        assert square.side == 20

    def test_set_side(self, square):
        square.side = 40
        assert square.side == 40

    def test_area(self, square):
        assert square.area == 20 * 20

    def test_perimiter(self, square):
        assert square.perimiter == 20 * 4
