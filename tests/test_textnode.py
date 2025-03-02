import unittest

from textnode import TextNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold", "url")
        node1 = TextNode("This is a text node", "bold", "url")
        self.assertEqual(node, node1)

    def test_diff_url_lead_to_non_equal(self):
        node = TextNode("Text", "bold", "url")
        node1 = TextNode("Text", "bold", "url1")

        self.assertNotEqual(node, node1)

    def test_dif_type_lead_to_non_equal(self):
        node = TextNode("Text", "bold", "url")
        node1 = TextNode("Text", "italic", "url")

        self.assertNotEqual(node, node1)


if __name__ == "__main__":
    unittest.main()
