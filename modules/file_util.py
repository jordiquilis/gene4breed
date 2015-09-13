import os


def get_file_extension(file_name):
    filename, file_extension = os.path.splitext(file_name)
    return file_extension
