import os
from os.path import isdir
from converters import markdown_to_html_node, extract_title


def copy_from_source_to_destination(source, destination):
    if not os.path.exists(destination):
        raise Exception(f"You shall not pass! ${destination} does not exist")
    if not os.path.exists(source):
        raise Exception(f"You shall not pass! ${source} does not exist")

    delete_files_from(destination)

    copy_files(source, destination)


def copy_files(source, destination):
    if os.path.isdir(source):
        if not os.path.exists(destination):
            os.makedirs(destination)

        for item in os.listdir(source):
            source_item = os.path.join(source, item)
            destination_item = os.path.join(destination, item)

            if os.path.isdir(source_item):
                copy_files(source_item, destination_item)
            else:
                copy_file(source_item, destination_item)
    else:
        copy_file(source, destination)


def copy_file(source, destination):
    try:
        with open(source, "rb") as src_file:
            with open(destination, "wb") as dst_file:
                while True:
                    chunk = src_file.read(1024 * 1024)
                    if not chunk:
                        break
                    dst_file.write(chunk)
    except Exception as e:
        print(
            f"You shall not pass! Failed to copy {source} to {destination}. Reason: {e}"
        )


def delete_files_from(path):
    if os.path.isfile(path) or os.path.islink((path)):
        os.unlink(path)
        return

    for filename in os.listdir(path):
        file_path = os.path.join(path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                delete_files_from(file_path)
                os.rmdir(file_path)
        except Exception as e:
            print("Failed to delete %s. Reason: %s" % (file_path, e))


def generate_page_recursive(base_path, dir_path_content, template_path, dest_dir_path):
    for item in os.listdir(dir_path_content):
        file_path = os.path.join(dir_path_content, item)
        if os.path.isdir(file_path):
            generate_page_recursive(base_path, file_path, template_path, dest_dir_path)
        elif file_path.endswith(".md"):
            relative_path = os.path.relpath(file_path, "content")
            dest_file_path = os.path.join(
                dest_dir_path, relative_path.replace(".md", ".html")
            )
            os.makedirs(os.path.dirname(dest_file_path), exist_ok=True)
            try:
                generate_page(base_path, file_path, template_path, dest_file_path)
            except Exception as e:
                print(f"Quebrou {file_path} por {e}")


def generate_page(base_path, from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path) as f:
        content = "".join(f.readlines())

    with open(template_path) as tf:
        template = "".join(tf.readlines())

    html_node = markdown_to_html_node(content)
    stringfied_html = html_node.to_html()
    title = extract_title(content)

    title_updated = template.replace("{{ Title }}", title)
    content_updated = (
        title_updated.replace("{{ Content }}", stringfied_html)
        .replace('href="/"', f'href="{base_path}"')
        .replace('src="/"', f'src="{base_path}"')
    )

    with open(dest_path, "w+") as df:
        df.write(content_updated)
        df.close()
