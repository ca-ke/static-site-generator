import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_repr(self):
        node = HTMLNode(
            tag="a", value="Visit Site", props={"href": "https://www.uol.com.br"}
        )

        self.assertEqual(
            f"{node}",
            "HTMLNode(a, Visit Site, None, {'href': 'https://www.uol.com.br'})",
        )

    def test_props_to_html(self):
        node = HTMLNode(
            tag="a",
            value="Visit Site",
            props={"href": "https://www.uol.com.br", "target": "_blank"},
        )

        self.assertEqual(
            node.props_to_html(), 'href="https://www.uol.com.br" target="_blank"'
        )
