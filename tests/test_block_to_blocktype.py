import unittest
from blocktype import BlockType
from src.converters import block_to_block_type


class TestBlockToBlockType(unittest.TestCase):
    def test_to_heading_block(self):
        current_value = block_to_block_type("# Heading")
        expected_value = BlockType("heading")

        self.assertEqual(expected_value, current_value)

    def test_to_ordered_list_block(self):
        current_value = block_to_block_type("1. First item\n2. Second item")
        expected_value = BlockType("ordered_list")

        self.assertEqual(expected_value, current_value)

    def test_to_code_block(self):
        current_value = block_to_block_type("```python\ndef foo():\n pass\n```")
        expected_value = BlockType("code")

        self.assertEqual(expected_value, current_value)

    def test_to_paragraph_block(self):
        current_value = block_to_block_type("Just a paragraph")
        expected_value = BlockType("paragraph")

        self.assertEqual(expected_value, current_value)

    def test_to_quote_block(self):
        current_value = block_to_block_type("> A first quote\n> A second quote")
        expected_value = BlockType("quote")

        self.assertEqual(current_value, expected_value)
