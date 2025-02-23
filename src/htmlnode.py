from typing import List, Optional


class HTMLNode:
    def __init__(
        self,
        tag: Optional[str] = None,
        value: Optional[str] = None,
        children: Optional[List["HTMLNode"]] = None,
        props: Optional[dict] = None,
    ):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self) -> str:
        if self.props is not None:
            return " ".join([f'{key}="{value}"' for key, value in self.props.items()])
        else:
            return ""

    def __eq__(self, value: object) -> bool:
        return (
            isinstance(value, HTMLNode)
            and value.tag == self.tag
            and value.value == self.value
            and value.children == self.children
            and value.props == self.props
        )

    def __repr__(self) -> str:
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
