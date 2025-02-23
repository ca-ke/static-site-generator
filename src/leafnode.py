from typing import Optional
from htmlnode import HTMLNode


class LeafNode(HTMLNode):
    def __init__(
        self,
        tag: Optional[str] = None,
        value: Optional[str] = None,
        props: Optional[dict] = None,
    ):
        super().__init__(tag=tag, props=props, children=None, value=value)

    def to_html(self) -> str:
        if not self.value:
            raise ValueError("All leaf nodes must have a value")
        if not self.tag:
            return self.value
        props_str = f" {self.props_to_html()}" if self.props else ""
        return f"<{self.tag}{props_str}>{self.value}</{self.tag}>"
