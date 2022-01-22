import os


def check_dir(directory: str):
    check_directory = os.path.isdir(directory)
    # If folder doesn't exist, then create it.
    if not check_directory:
        os.makedirs(directory)
