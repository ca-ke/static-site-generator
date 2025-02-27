from htmlnode import HTMLNode
from parentnode import ParentNode
from leafnode import LeafNode
from textnode import TextNode
from textype import TextType
from blocktype import BlockType
import re


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
            raise Exception(f"Delimiter {delimiter} must be closed - {node.text}")

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
                    delimiter="_",
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
    elif all(line.strip().startswith(">") for line in block.split("\n")):
        return BlockType.QUOTE
    elif all(line.strip().startswith(("- ")) for line in block.split("\n")):
        return BlockType.UNORDERED_LIST
    elif all(re.match(r"^\d+\.\s", line.strip()) for line in block.split("\n")):
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children


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
                ParentNode(
                    tag=f"h{heading_level}",
                    children=text_to_children(heading_text),
                )
            )
        elif block_type == BlockType.PARAGRAPH:
            result.append(
                ParentNode(tag="p", children=text_to_children(element.strip()))
            )
        elif block_type == BlockType.CODE:
            code_content = "\n".join(
                line for line in element.splitlines() if not line.startswith("```")
            )
            result.append(
                ParentNode(
                    tag="pre",
                    children=[
                        ParentNode(tag="code", children=text_to_children(code_content))
                    ],
                )
            )
        elif block_type == BlockType.UNORDERED_LIST:
            list_items = [
                ParentNode(tag="li", children=text_to_children(line[2:]))
                for line in element.splitlines()
                if line.strip()
            ]
            result.append(ParentNode(tag="ul", children=list_items))
        elif block_type == BlockType.ORDERED_LIST:
            list_item = [
                ParentNode(
                    tag="li",
                    children=text_to_children(re.sub(r"^\d+\.\s", "", line).strip()),
                )
                for line in element.splitlines()
                if line.strip()
            ]
            result.append(ParentNode(tag="ol", children=list_item))
        elif block_type == BlockType.QUOTE:
            quote_lines = [line.lstrip(">").strip() for line in element.splitlines()]
            quote_content = " ".join(quote_lines)
            result.append(
                ParentNode(tag="blockquote", children=text_to_children(quote_content))
            )

    return ParentNode(tag="div", children=result)


def extract_title(markdown):
    splitted_doc = markdown.splitlines()
    h1_elements = [element for element in splitted_doc if element.startswith("# ")]
    contains_h1 = len(h1_elements) > 0
    if not contains_h1:
        raise Exception()

    return h1_elements[0].split("#")[-1].strip()
