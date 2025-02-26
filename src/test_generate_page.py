import unittest

from converters import generate_page


class TestGeneratePage(unittest.TestCase):
    def test_generate_content(self):
        print("\n")
        generate_page("content/index.md", "template.html", "public/index.html")
