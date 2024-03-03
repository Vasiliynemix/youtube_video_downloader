import os
from urllib.parse import urlparse


def is_valid_url(url) -> bool:
    try:
        urlparse(url)
        return True
    except ValueError:
        return False


def check_file_exists(file_path: str) -> bool:
    return os.path.isfile(file_path)
