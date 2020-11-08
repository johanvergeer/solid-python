import pytest

from python_solid_principles.jas.formatting import format_amount


@pytest.mark.parametrize(
    "amount,expected",
    [
        (1, "€    1.00"),
        (1.23, "€    1.23"),
        (1.2345, "€    1.23"),
        (1.2365, "€    1.24"),
    ],
)
def test_format_amount__default_values(amount, expected):
    assert format_amount(amount) == expected


def test_format_amount__different_symbol():
    assert format_amount(1, symbol="$") == "$    1.00"


@pytest.mark.parametrize("length,expected", [
    (0, "€ 1.00"),
    (1, "€ 1.00"),
    (6, "€ 1.00"),
    (7, "€  1.00"),
])
def test_format_amount__different_length(length, expected):
    assert format_amount(1, length=length) == expected
