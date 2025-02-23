from typing import Optional
from textype import TextType


class TextNode:
    def __init__(self, text: str, text_type: str, url: Optional[str] = None):
        self.text = text
        self.text_type = TextType(text_type)
        self.url = url

    def __eq__(self, other) -> bool:
        return (
            isinstance(other, TextNode)
            and self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        )

    def __repr__(self) -> str:
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
