"""Unit tests for task.py conversion functions."""

import unittest
from task import conv_num, my_datetime, conv_endian


class TestConvNum(unittest.TestCase):
    """Black-box and edge-case tests for conv_num."""

    def test_positive_integer(self):
        self.assertEqual(conv_num('12345'), 12345)
        self.assertIsInstance(conv_num('12345'), int)

    def test_negative_float(self):
        self.assertEqual(conv_num('-123.45'), -123.45)
        self.assertIsInstance(conv_num('-123.45'), float)

    def test_leading_decimal(self):
        self.assertEqual(conv_num('.45'), 0.45)

    def test_trailing_decimal(self):
        self.assertEqual(conv_num('123.'), 123.0)
        self.assertIsInstance(conv_num('123.'), float)

    def test_hex_uppercase_prefix(self):
        self.assertEqual(conv_num('0xAD4'), 2772)

    def test_hex_mixed_case(self):
        self.assertEqual(conv_num('0Xad4'), 2772)

    def test_negative_hex(self):
        self.assertEqual(conv_num('-0xAD4'), -2772)
        self.assertIsInstance(conv_num('-0xAD4'), int)

    def test_invalid_hex_digit(self):
        self.assertIsNone(conv_num('0xAZ4'))

    def test_alpha_without_hex_prefix(self):
        self.assertIsNone(conv_num('12345A'))

    def test_multiple_decimals(self):
        self.assertIsNone(conv_num('12.3.45'))

    def test_empty_string(self):
        self.assertIsNone(conv_num(''))

    def test_non_string(self):
        self.assertIsNone(conv_num(12345))
        self.assertIsNone(conv_num(None))
        self.assertIsNone(conv_num(['1']))

    def test_bare_minus(self):
        self.assertIsNone(conv_num('-'))

    def test_bare_decimal_point(self):
        self.assertIsNone(conv_num('.'))
        self.assertIsNone(conv_num('-.'))

    def test_hex_without_digits(self):
        self.assertIsNone(conv_num('0x'))
        self.assertIsNone(conv_num('-0X'))

    def test_hex_with_decimal_point(self):
        self.assertIsNone(conv_num('0xFF.02'))

    def test_zero_values(self):
        self.assertEqual(conv_num('0'), 0)
        self.assertEqual(conv_num('0.0'), 0.0)
        self.assertEqual(conv_num('0x0'), 0)

    def test_negative_integer(self):
        self.assertEqual(conv_num('-42'), -42)
        self.assertIsInstance(conv_num('-42'), int)

    def test_negative_leading_decimal(self):
        self.assertEqual(conv_num('-.5'), -0.5)


class TestMyDatetime(unittest.TestCase):
    """Tests for epoch-seconds to date conversion, including leap years."""

    def test_epoch(self):
        self.assertEqual(my_datetime(0), '01-01-1970')

    def test_example_1973(self):
        self.assertEqual(my_datetime(123456789), '11-29-1973')

    def test_example_2282(self):
        self.assertEqual(my_datetime(9876543210), '12-22-2282')

    def test_leap_day_far_future(self):
        self.assertEqual(my_datetime(201653971200), '02-29-8360')

    def test_one_day(self):
        self.assertEqual(my_datetime(86400), '01-02-1970')

    def test_end_of_non_leap_feb(self):
        # 1970 is not a leap year; day 58 (0-based from Jan 1) = Feb 28
        self.assertEqual(my_datetime(58 * 86400), '02-28-1970')
        self.assertEqual(my_datetime(59 * 86400), '03-01-1970')

    def test_leap_year_1972(self):
        # 1972 is a leap year. Days from 1970-01-01 to 1972-02-29:
        # 1970+1971 = 730 days, then Jan + Feb 1-28 = 59 -> Feb 29
        leap_day = (365 + 365 + 31 + 28) * 86400
        self.assertEqual(my_datetime(leap_day), '02-29-1972')

    def test_year_2000_leap(self):
        # 2000 is divisible by 400, so it is a leap year
        # Verify Feb 29, 2000 exists via known offset from a nearby date
        # Days from 1970-01-01 to 2000-02-29:
        # years 1970-1999 inclusive = 30 years
        days = 0
        year = 1970
        while year < 2000:
            days = days + (366 if (year % 400 == 0 or
                                   (year % 4 == 0 and year % 100 != 0))
                           else 365)
            year = year + 1
        days = days + 31 + 28  # Jan + Feb 1-28 -> lands on Feb 29
        self.assertEqual(my_datetime(days * 86400), '02-29-2000')


class TestConvEndian(unittest.TestCase):
    """Tests for integer to endian-aware hex byte string conversion."""

    def test_big_endian_explicit(self):
        self.assertEqual(conv_endian(954786, 'big'), '0E 91 A2')

    def test_big_endian_default(self):
        self.assertEqual(conv_endian(954786), '0E 91 A2')

    def test_negative_big_endian(self):
        self.assertEqual(conv_endian(-954786), '-0E 91 A2')

    def test_little_endian(self):
        self.assertEqual(conv_endian(954786, 'little'), 'A2 91 0E')

    def test_negative_little_endian(self):
        self.assertEqual(conv_endian(-954786, 'little'), '-A2 91 0E')

    def test_keyword_args(self):
        self.assertEqual(
            conv_endian(num=-954786, endian='little'),
            '-A2 91 0E'
        )

    def test_invalid_endian(self):
        self.assertIsNone(conv_endian(num=-954786, endian='small'))
        self.assertIsNone(conv_endian(1, 'BIG'))
        self.assertIsNone(conv_endian(1, ''))

    def test_zero(self):
        self.assertEqual(conv_endian(0), '00')
        self.assertEqual(conv_endian(0, 'little'), '00')

    def test_single_byte(self):
        self.assertEqual(conv_endian(255), 'FF')
        self.assertEqual(conv_endian(15), '0F')

    def test_negative_single_byte(self):
        self.assertEqual(conv_endian(-255), '-FF')


if __name__ == '__main__':
    unittest.main()
