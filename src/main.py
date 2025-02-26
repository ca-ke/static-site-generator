from textnode import TextNode
from utils import copy_from_source_to_destination, delete_files_from
from converters import generate_page


def main():
    delete_files_from("public")
    copy_from_source_to_destination("static", "public")
    generate_page("content/index.md", "template.html", "public/index.html")


if __name__ == "__main__":
    main()
