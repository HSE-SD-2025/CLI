import os
import os.path
from os import PathLike


class FileSystem:
    def __init__(self):
        self.current_dir = os.getcwd()

    def get_current_dir(self):
        return self.current_dir

    def resolve(self, path: PathLike):
        expanded_path = os.path.expanduser(path)
        if os.path.isabs(expanded_path):
            abs_path = expanded_path
        else:
            abs_path = os.path.join(self.current_dir, expanded_path)
        normalized_path = os.path.normpath(abs_path)
        return normalized_path

    def set_current_dir(self, path):
        self.current_dir = path
