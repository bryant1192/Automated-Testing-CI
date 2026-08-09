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

    if len(hex_string) % 2 != 0:
        hex_string = "0" + hex_string

    bytes_list = []

    for i in range(0, len(hex_string), 2):
        bytes_list.append(hex_string[i:i + 2])

    if endian == 'little':
        bytes_list.reverse()

    result = " ".join(bytes_list)

    if is_negative:
        result = "-" + result

    return result