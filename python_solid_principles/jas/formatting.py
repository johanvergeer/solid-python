def format_amount(amount: float, symbol: str = "€", length: int = 9):
    """Format an amount to a string

    Args:
        amount: The amount to be formatted
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

        >>> format_amount(123.45, symbol="$")
        "$  123.45"

        >>> format_amount(123.45, length=12)
        "$     123.45"

        >>> format_amount(123.45, length=0)
        "$ 123.45"

    """
    return f"{symbol} " + ("{:.2f}".format(amount)).rjust(length - 2)
