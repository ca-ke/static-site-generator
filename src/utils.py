import os
from os.path import isdir


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
