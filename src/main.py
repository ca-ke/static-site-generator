from textnode import TextNode
from utils import (
    copy_from_source_to_destination,
    delete_files_from,
    generate_page_recursive,
)
import sys


def main():
    basepath = "/" if len(sys.argv) < 2 else sys.argv[1]

    delete_files_from("doc")
    copy_from_source_to_destination("static", "doc")
    generate_page_recursive(basepath, "content", "template.html", "doc")


if __name__ == "__main__":
    main()
