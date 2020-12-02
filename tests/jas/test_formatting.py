from datetime import date, datetime

import pytest

from python_solid_principles.jas.formatting import (
    format_amount,
    format_date,
    format_string,
)


class TestFormatAmount:
    @pytest.mark.parametrize(
        "amount,expected",
        [
            (1, "€    1.00"),
            (1.23, "€    1.23"),
            (1.2345, "€    1.23"),
            (1.2365, "€    1.24"),
        ],
    )
    def test_format_amount__default_values(self, amount, expected):
        assert format_amount(amount) == expected

    def test_format_amount__different_symbol(self):
        assert format_amount(1, symbol="$") == "$    1.00"

    @pytest.mark.parametrize(
        "length,expected",
        [
            (0, "€ 1.00"),
            (1, "€ 1.00"),
            (6, "€ 1.00"),
            (7, "€  1.00"),
        ],
    )
    def test_format_amount__different_length(self, length, expected):
        assert format_amount(1, length=length) == expected


@pytest.mark.parametrize(
    "input,length,expected",
    [
        ("input value", 11, "input value"),
        ("input value", 10, "input valu"),
        ("input value", 12, "input value "),
    ],
)
def test_format_string(input, length, expected):
    assert format_string(input, length) == expected


@pytest.mark.parametrize(
    "input,length,expected",
    [
        (date(2020, 10, 10), 10, "2020-10-10"),
        (date(2020, 10, 10), 11, "2020-10-10 "),
        (date(2020, 10, 10), 9, "2020-10-10"),
        (date(2020, 7, 7), 10, "2020-07-07"),
    ],
)
def test_format_date(input, length, expected):
    assert format_date(input, length) == expected
