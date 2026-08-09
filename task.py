def conv_endian(num, endian='big'):
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