from typing import List
from htmlnode import HTMLNode
from leafnode import LeafNode
from textnode import TextNode
from textype import TextType
from blocktype import BlockType
import re
import functools


def text_node_to_html_node(text_node: TextNode) -> HTMLNode:
    match text_node.text_type:
        case TextType.NORMAL_TEXT:
            return LeafNode(value=text_node.text)
        case TextType.BOLD_TEXT:
            return LeafNode(tag="b", value=text_node.text)
        case TextType.ITALIC_TEXT:
            return LeafNode(tag="i", value=text_node.text)
        case TextType.CODE_TEXT:
            return LeafNode(tag="code", value=text_node.text)
        case TextType.LINK_TEXT:
            return LeafNode(
                tag="a",
                value=text_node.text,
                props={"href": text_node.url},
            )
        case TextType.IMAGE_TEXT:
            return LeafNode(
                tag="img", value="", props={"src": text_node.url, "alt": text_node.text}
            )


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    result = []
    pattern = f"({re.escape(delimiter)})"
    for node in old_nodes:
        if node.text_type != TextType.NORMAL_TEXT:
            result.append(node)
            continue

        if node.text.count(delimiter) % 2 != 0:
            raise Exception("Delimiter must be closed")

        splitted_node_text = re.split(pattern, node.text)
        waiting_for_close = False
        for text in splitted_node_text:
            if text == delimiter:
                waiting_for_close = not waiting_for_close
                continue
            else:
                current_type = text_type if waiting_for_close else "normal"
                result.append(TextNode(text=text, text_type=current_type))

    return result


def extract_markdown_images(text):
    pattern = r"!\[(.*?)\]\((.*?)\)"
    return re.findall(pattern, text)


def extract_markdown_links(text):
    pattern = r"(?<!!)\[(.*?)\]\((.*?)\)"
    return re.findall(pattern, text)


def markdown_to_blocks(markdown):
    result = []
    splitted_lines = [item.strip() for item in markdown.split("\n")]
    current_block = []
    for line in splitted_lines:
        if line != "":
            current_block.append(line)
        else:
            if len(current_block) > 0:
                result.append("\n".join(current_block))
                current_block = []

    if len(current_block) > 0:
        result.append("\n".join(current_block))
    return result


def text_to_textnodes(text):
    return split_nodes_link(
        split_nodes_image(
            split_nodes_delimiter(
                split_nodes_delimiter(
                    split_nodes_delimiter(
                        [TextNode(text, "normal")],
                        delimiter="**",
                        text_type="bold",
                    ),
                    delimiter="*",
                    text_type="italic",
                ),
                delimiter="`",
                text_type="code",
            )
        )
    )


def split_nodes_image(old_nodes):
    result = []
    for node in old_nodes:
        images = extract_markdown_images(node.text)
        if not images:
            result.append(TextNode(node.text, node.text_type))
            continue

        current_text = node.text
        for image_tuple in images:
            image_description, url = image_tuple
            markdown_image = f"![{image_description}]({url})"
            parts = current_text.split(markdown_image, 1)

            if parts[0]:
                result.append(TextNode(parts[0], "normal"))
            result.append(TextNode(image_description, "image", url))

            current_text = parts[1]

        if current_text:
            result.append(TextNode(current_text, "normal"))

    return result


def split_nodes_link(old_nodes):
    result = []
    for node in old_nodes:
        links = extract_markdown_links(node.text)
        if not links:
            result.append(TextNode(node.text, node.text_type))
            continue

        current_text = node.text
        for link_tuple in links:
            link_text, url = link_tuple
            markdown_link = f"[{link_text}]({url})"
            parts = current_text.split(markdown_link, 1)

            if parts[0]:
                result.append(TextNode(parts[0], "normal"))
            result.append(TextNode(link_text, "link", url))

            current_text = parts[1]

        if current_text:
            result.append(TextNode(current_text, "normal"))
    return result


def block_to_block_type(block) -> BlockType:
    if re.match(r"^#+\s", block.strip()):
        return BlockType.HEADING
    elif block.strip().startswith("```") and block.strip().endswith("```"):
        return BlockType.CODE
    elif all(line.strip().startswith("> ") for line in block.split("\n")):
        return BlockType.QUOTE
    elif all(line.strip().startswith(("* ", "- ")) for line in block.split("\n")):
        return BlockType.UNORDERED_LIST
    elif all(re.match(r"^\d+\.\s", line.strip()) for line in block.split("\n")):
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH


def markdown_to_html_node(markdown):
    splitted_markdown = markdown_to_blocks(markdown)
    print(splitted_markdown)
    result = []
    for element in splitted_markdown:
        block_type = block_to_block_type(element)
        if block_type == BlockType.HEADING:
            heading_level = element.count("#", 0, element.index(" "))
            heading_text = element.lstrip("# ").strip()
            result.append(
                HTMLNode(
                    tag=f"h{heading_level}",
                    value=heading_text,
                )
            )
        elif block_type == BlockType.PARAGRAPH:
            result.append(HTMLNode(tag="p", value=element.strip()))
        elif block_type == BlockType.CODE:
            code_content = "\n".join(
                line for line in element.splitlines() if not line.startswith("```")
            )
            result.append(
                HTMLNode(tag="pre", children=[HTMLNode(tag="code", value=code_content)])
            )
        elif block_type == BlockType.UNORDERED_LIST:
            list_items = [
                HTMLNode(tag="li", value=line.lstrip("*- ").strip())
                for line in element.splitlines()
                if line.strip()
            ]
            result.append(HTMLNode(tag="ul", children=list_items))
        elif block_type == BlockType.ORDERED_LIST:
            list_item = [
                HTMLNode(tag="li", value=re.sub(r"^\d+\.\s", "", line).strip())
                for line in element.splitlines()
                if line.strip()
            ]
            result.append(HTMLNode(tag="ol", children=list_item))
        elif block_type == BlockType.QUOTE:
            quote_lines = [line.lstrip("> ").strip() for line in element.splitlines()]
            quote_content = "\n".join(quote_lines)
            result.append(HTMLNode(tag="blockquote", value=quote_content))

    return HTMLNode(tag="div", children=result)
