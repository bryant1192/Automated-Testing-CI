def conv_endian(num, endian='big'):
    if endian != 'big' and endian != 'little':
        return None

    is_negative = False

    if num < 0:
        is_negative = True
        num = -num