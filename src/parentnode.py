from typing import Optional
from htmlnode import HTMLNode


class ParentNode(HTMLNode):
    def __init__(
        self,
        tag: str,
        children: list,
        props: Optional[dict] = None,
    ):
        super().__init__(
            tag=tag,
            children=children,
            props=props,
        )

    def to_html(self):
        if not self.tag:
            raise ValueError("Tag must not be empty")
        if not self.children:
            raise ValueError("Children must not be null")

        props_str = f" {self.props_to_html()}" if self.props else ""
        children_html = "".join(child.to_html() for child in self.children)

        if not self.children:
            return f"<{self.tag}{props_str}>{self.value}</{self.tag}>"
        return f"<{self.tag}{props_str}>{children_html}</{self.tag}>"
