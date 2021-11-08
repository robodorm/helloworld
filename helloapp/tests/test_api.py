import unittest

from helloapp.app import is_valid_date_format


class TestApi(unittest.TestCase):
    """
    Test the API's is_valid_date_format function.
    """

    def test_is_valid_date_format(self):
        self.assertTrue(is_valid_date_format('2018-01-01'))
        self.assertFalse(is_valid_date_format(''))
        self.assertFalse(is_valid_date_format(None))
        self.assertFalse(is_valid_date_format('0'))
        self.assertFalse(is_valid_date_format(0))
        self.assertFalse(is_valid_date_format('2018-01-01T00:00:00'))
        self.assertFalse(is_valid_date_format('2018-01-01T00:00:00Z'))
        self.assertFalse(is_valid_date_format('2018-01-01T00:00:00+00:00'))
        self.assertFalse(is_valid_date_format('2018-01-01T00:00:00+00:00Z'))
        self.assertFalse(is_valid_date_format('2018-01-01T00:00:00+00:00:00'))
        self.assertFalse(is_valid_date_format('2018-01-01T00:00:00+00:00:00Z'))
        self.assertFalse(is_valid_date_format('2018-01-01T00:00:00+00:00:00+00:00'))
        self.assertFalse(is_valid_date_format('2018-01-01T00:00:00+00:00:00+00:00Z'))
        self.assertFalse(is_valid_date_format('2018-01-01T00:00:00+00:00:00+00:00:00'))
        self.assertFalse(is_valid_date_format('2018-01-01T00:00:00+00:00:00+00:00:00Z'))
        self.assertFalse(is_valid_date_format('2018-01-01T00:00:00+00:00:00+00:00:00+00:00'))
