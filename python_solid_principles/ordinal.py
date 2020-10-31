def ordinal(number: int) -> str:
    """Converts zero or a 'postive' integer to an ordinal value"""
    if number == 11 or number == 12 or number == 13:
        return f"{number}th"
    if number % 10 == 1:
        return f"{number}st"
    if number % 10 == 2:
        return f"{number}nd"
    if number % 10 == 3:
        return f"{number}rd"
    return f"{number}th"
