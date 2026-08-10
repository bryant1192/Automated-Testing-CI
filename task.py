"""CS362 Group Project Part 2 - number, datetime, and endian conversions."""


def _hex_digit_value(char):
    """Return 0-15 for a hex digit character, or None if invalid."""
    if '0' <= char <= '9':
        return ord(char) - ord('0')
    if 'a' <= char <= 'f':
        return ord(char) - ord('a') + 10
    if 'A' <= char <= 'F':
        return ord(char) - ord('A') + 10
    return None


def _dec_digit_value(char):
    """Return 0-9 for a decimal digit character, or None if invalid."""
    if '0' <= char <= '9':
        return ord(char) - ord('0')
    return None


def _parse_hex_string(hex_body, negative):
    """Parse a hexadecimal integer body (no 0x prefix). Returns int or None."""
    if hex_body == '':
        return None

    value = 0
    for char in hex_body:
        digit = _hex_digit_value(char)
        if digit is None:
            return None
        value = value * 16 + digit

    if negative:
        return -value
    return value


def _parse_decimal_string(body, negative):
    """Parse a base-10 integer or float string body.

    Returns int, float, or None.
    """
    if body == '':
        return None

    dot_count = 0
    for char in body:
        if char == '.':
            dot_count = dot_count + 1
        elif _dec_digit_value(char) is None:
            return None

    if dot_count > 1:
        return None

    if dot_count == 0:
        # Integer path
        value = 0
        for char in body:
            value = value * 10 + _dec_digit_value(char)
        if negative:
            return -value
        return value

    # Float path — must contain at least one digit somewhere
    parts = body.split('.')
    whole_str = parts[0]
    frac_str = parts[1]

    if whole_str == '' and frac_str == '':
        return None

    whole = 0
    for char in whole_str:
        whole = whole * 10 + _dec_digit_value(char)

    frac = 0.0
    place = 10.0
    for char in frac_str:
        frac = frac + _dec_digit_value(char) / place
        place = place * 10.0

    value = whole + frac
    if negative:
        return -value
    return value


def conv_num(num_str):
    """Convert a numeric string to an int or float.

    Invalid input returns None.
    """
    if not isinstance(num_str, str) or num_str == '':
        return None

    negative = False
    start = 0
    if num_str[0] == '-':
        negative = True
        start = 1
        if len(num_str) == 1:
            return None

    body = num_str[start:]

    # Hexadecimal: optional leading '-', then 0x / 0X, then hex digits only
    is_hex = (
        len(body) >= 2
        and body[0] == '0'
        and (body[1] == 'x' or body[1] == 'X')
    )
    if is_hex:
        return _parse_hex_string(body[2:], negative)

    return _parse_decimal_string(body, negative)


def _is_leap_year(year):
    """Return True if year is a Gregorian leap year."""
    if year % 400 == 0:
        return True
    if year % 100 == 0:
        return False
    if year % 4 == 0:
        return True
    return False


def _days_in_month(year, month):
    """Return the number of days in the given month of year."""
    if month == 2:
        if _is_leap_year(year):
            return 29
        return 28
    if month in (4, 6, 9, 11):
        return 30
    return 31


def _pad_two(number):
    """Zero-pad an integer to two characters."""
    text = str(number)
    if len(text) < 2:
        return '0' + text
    return text


def my_datetime(num_sec):
    """Convert seconds since 1970-01-01 epoch to 'MM-DD-YYYY'."""
    seconds_per_day = 24 * 60 * 60
    days = num_sec // seconds_per_day

    year = 1970
    while True:
        days_in_year = 366 if _is_leap_year(year) else 365
        if days < days_in_year:
            break
        days = days - days_in_year
        year = year + 1

    month = 1
    while True:
        dim = _days_in_month(year, month)
        if days < dim:
            break
        days = days - dim
        month = month + 1

    day = days + 1
    return _pad_two(month) + '-' + _pad_two(day) + '-' + str(year)


def conv_endian(num, endian='big'):
    """Convert an integer to a space-separated hex byte string."""
    if endian != 'big' and endian != 'little':
        return None

    is_negative = False

    if num < 0:
        is_negative = True
        num = -num

    hex_digits = "0123456789ABCDEF"
    hex_string = ""

    if num == 0:
        hex_string = "00"
    else:
        while num > 0:
            remainder = num % 16
            hex_string = hex_digits[remainder] + hex_string
            num = num // 16

    # Each byte is two hex characters; pad leading nibble if needed
    if len(hex_string) % 2 == 1:
        hex_string = '0' + hex_string

    bytes_list = []
    index = 0
    while index < len(hex_string):
        bytes_list.append(hex_string[index:index + 2])
        index = index + 2

    if endian == 'little':
        bytes_list = bytes_list[::-1]

    result = ' '.join(bytes_list)
    if is_negative:
        return '-' + result
    return result

