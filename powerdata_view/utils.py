import unicodedata
import re
import os


def make_dir(path, dir_name):
    """Creates a directory `dir_name` if path is not None and if directory does not already exist."""
    if path is not None:
        dir_path = os.path.join(path, dir_name)
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)
    else:
        dir_path = None
    return dir_path


def slugify(value):
    """Taken from https://github.com/django/django/blob/master/django/utils/text.py"""
    value = str(value)
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value.lower())
    return re.sub(r'[-\s]+', '-', value).strip('-_')
