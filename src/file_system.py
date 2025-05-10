import os
import os.path


class FileSystem:
    def __init__(self):
        self.currend_dir = os.getcwd()

    def get_current_dir(self):
        return self.currend_dir

    def resolve(self, path):
        if os.path.isabs(path):
            return path
        return os.path.join(self.currend_dir, path)
