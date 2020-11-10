from datetime import datetime, date
from typing import Union


def format_any(value: Union[str, int, float, date], length):
    if isinstance(value, date):
        return format_date(value, length)
    if isinstance(value, (int, float)):
        return format_number(value, length)
    else:
        return format_string(value, length)


def format_string(value: str, lenght: int):
    return value[:lenght].ljust(lenght)


def format_number(value: Union[int, float], length):
    return str(value).ljust(length)


def format_date(value: date, length: int):
    return str(value).ljust(length)


def format_amount(value: float, length: int = 9, symbol: str = "€"):
    """Format an amount to a string

    Args:
        value: The amount to be formatted
        symbol: Currency symbol
        length: **Minimum** length of the formatted string.
        If the length is to short to fit the amount, then the formatted string
        will be longer.

    Returns:
        The amount formatted as a string.

    Examples:
        >>> format_amount(1)
        "€    1.00"

        >>> format_amount(123.45)
        "€  123.45"

        >>> format_amount(123.45,symbol="$")
        "$  123.45"

        >>> format_amount(123.45,length=12)
        "$     123.45"

        >>> format_amount(123.45,length=0)
        "$ 123.45"

    """
    return f"{symbol} " + ("{:.2f}".format(value)).rjust(length - 2)
