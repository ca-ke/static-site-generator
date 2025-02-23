import unittest
from converters import markdown_to_html_node
from htmlnode import HTMLNode


class TestMarkdownToHtmlNode(unittest.TestCase):
    def test_markdown_to_html_node(self):
        markdown = """
        # Header
        
        ## Second Header
        """

        current_value = markdown_to_html_node(markdown)
        expected_value = HTMLNode(
            tag="div",
            children=[
                HTMLNode(tag="h1", value="Header"),
                HTMLNode(tag="h2", value="Second Header"),
            ],
        )

        self.assertEqual(current_value, expected_value)

    def test_markdown_to_html_node_1(self):
        markdown = """
        # Header
        
        ## Second Header

        ```
            def foo():
                print("Oi")
        ```
        """

        current_value = markdown_to_html_node(markdown)

        print("\n")
        print("-----------------\n")
        print(current_value)
        print("\n-----------------")
        print("\n")

        expected_value = HTMLNode(
            tag="div",
            children=[
                HTMLNode(tag="h1", value="Header"),
                HTMLNode(tag="h2", value="Second Header"),
                HTMLNode(
                    tag="pre",
                    children=[HTMLNode(tag="code", value='def foo():\nprint("Oi")')],
                ),
            ],
        )

        self.assertEqual(current_value, expected_value)
