import unittest

from converters import extract_title


class TestExtractTitle(unittest.TestCase):
    def test_extract_title(self):
        markdown = "# Hello"
        current_value = extract_title(markdown)
        expected_value = "Hello"

        self.assertEqual(current_value, expected_value)

    def test_extract_title_with_error(self):
        markdown = "Hello"
        self.assertRaises(Exception, lambda _: extract_title(markdown))
