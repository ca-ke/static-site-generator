import unittest

from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_to_html_without_value_should_raise_exception(self):
        node = LeafNode(tag="a", value="", props={})
        self.assertRaises(ValueError, node.to_html)

    def test_to_html_with_value_should_return_expected_value(self):
        node = LeafNode("p", "This is a paragraph of text.")
        self.assertEqual("<p>This is a paragraph of text.</p>", node.to_html())

    def test_to_html_with_value_and_props_should_return_expected_value(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(
            '<a href="https://www.google.com">Click me!</a>', node.to_html()
        )
