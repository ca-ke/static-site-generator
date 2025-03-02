import unittest

from textnode import TextNode
from src.converters import (
    text_node_to_html_node,
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_link,
    split_nodes_image,
    text_to_textnodes,
    markdown_to_blocks,
)
from htmlnode import HTMLNode


class TestTransformers(unittest.TestCase):
    def test_text_transformation(self):
        result = text_node_to_html_node(TextNode(text="Texto", text_type="normal"))
        self.assertEqual(HTMLNode(value="Texto"), result)

    def test_bold_transformation(self):
        result = text_node_to_html_node(TextNode(text="Texto", text_type="bold"))
        self.assertEqual(result, HTMLNode(tag="b", value="Texto"))

    def test_split_node_with_code_block(self):
        node = TextNode("This is text with a `code block` word", "normal")
        new_nodes = split_nodes_delimiter([node], "`", "code")
        self.assertEqual(
            [
                TextNode("This is text with a ", "normal"),
                TextNode("code block", "code"),
                TextNode(" word", "normal"),
            ],
            new_nodes,
        )

    def test_split_node_with_bold_text(self):
        node = TextNode("This is **bold** text", "normal")
        new_nodes = split_nodes_delimiter([node], "**", "bold")
        self.assertEqual(
            [
                TextNode("This is ", "normal"),
                TextNode("bold", "bold"),
                TextNode(" text", "normal"),
            ],
            new_nodes,
        )

    def test_split_node_with_unclosed_delimiter(self):
        node = TextNode("This is **bold test", "normal")
        self.assertRaises(
            Exception, lambda _: split_nodes_delimiter([node], "**", "bold")
        )

    def test_split_node_with_italic_text(self):
        node = TextNode("Here is *italic* text", "normal")
        new_nodes = split_nodes_delimiter([node], "*", "italic")
        self.assertEqual(
            [
                TextNode(text="Here is ", text_type="normal"),
                TextNode(text="italic", text_type="italic"),
                TextNode(text=" text", text_type="normal"),
            ],
            new_nodes,
        )

    def test_split_node_with_empty_string(self):
        node = TextNode("", "normal")
        new_nodes = split_nodes_delimiter([node], "**", "bold")
        self.assertEqual([TextNode(text="", text_type="normal")], new_nodes)

    def test_extract_markdown_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        current_value = extract_markdown_images(text)
        self.assertEqual(
            current_value,
            [
                ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
                ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
            ],
        )

    def test_extract_markdown_images_1(self):
        text = "This is text with a [rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        current_value = extract_markdown_images(text)
        self.assertEqual(
            current_value,
            [
                ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
            ],
        )

    def test_extract_markdown_links(self):
        text = "This is text with a [rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        current_value = extract_markdown_links(text)
        self.assertEqual(
            current_value,
            [
                ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
            ],
        )

    def test_split_node_links_with_multiple_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            "normal",
        )
        new_nodes = split_nodes_link([node])

        self.assertEqual(
            [
                TextNode(text="This is text with a link ", text_type="normal"),
                TextNode(
                    text="to boot dev", text_type="link", url="https://www.boot.dev"
                ),
                TextNode(text=" and ", text_type="normal"),
                TextNode(
                    text="to youtube",
                    text_type="link",
                    url="https://www.youtube.com/@bootdotdev",
                ),
            ],
            new_nodes,
        )

    def test_split_node_links_single_link(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev)", "normal"
        )
        new_nodes = split_nodes_link([node])

        self.assertEqual(
            [
                TextNode(text="This is text with a link ", text_type="normal"),
                TextNode(
                    text="to boot dev", text_type="link", url="https://www.boot.dev"
                ),
            ],
            new_nodes,
        )

    def test_split_node_links_without_links(self):
        node = TextNode("This is text with a link", "normal")
        new_nodes = split_nodes_link([node])

        self.assertEqual(
            [
                TextNode(text="This is text with a link", text_type="normal"),
            ],
            new_nodes,
        )

    def test_split_node_images_with_multiple_images(self):
        node = TextNode(
            "This is text with a link ![to boot dev](https://www.boot.dev) and ![to youtube](https://www.youtube.com/@bootdotdev)",
            "normal",
        )
        new_nodes = split_nodes_image([node])

        self.assertEqual(
            [
                TextNode(text="This is text with a link ", text_type="normal"),
                TextNode(
                    text="to boot dev", text_type="image", url="https://www.boot.dev"
                ),
                TextNode(text=" and ", text_type="normal"),
                TextNode(
                    text="to youtube",
                    text_type="image",
                    url="https://www.youtube.com/@bootdotdev",
                ),
            ],
            new_nodes,
        )

    def test_split_text_to_textnode(self):
        print("\n")
        text = "This is **bold** and *italic* text"
        nodes = text_to_textnodes(text)
        print(nodes)

    def test_markdown_to_text(self):
        text = """
        This is a paragraph of text. It has some **bold** and *italic* words inside of it.
            
        * This is the first list item in a list block
        * This is a list item
        * This is another list item
    """

        current_value = markdown_to_blocks(text)
        expected_value = [
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
            "* This is the first list item in a list block\n* This is a list item\n* This is another list item",
        ]

        self.assertEqual(current_value, expected_value)

    def test_markdown_to_text_1(self):
        text = """
        * This is the first list item in a list block
        * This is a list item


        * This is another list item
    """

        current_value = markdown_to_blocks(text)

        expected_value = [
            "* This is the first list item in a list block\n* This is a list item",
            "* This is another list item",
        ]

        self.assertEqual(current_value, expected_value)
