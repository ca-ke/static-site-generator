from textnode import TextNode
from utils import (
    copy_from_source_to_destination,
    delete_files_from,
    generate_page_recursive,
)


def main():
    delete_files_from("public")
    copy_from_source_to_destination("static", "public")

    generate_page_recursive("content", "template.html", "public")


if __name__ == "__main__":
    main()
