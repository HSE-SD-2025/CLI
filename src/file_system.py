import os

class FileSystem:
    def __init__(self):
        self.currend_dir = os.getcwd()
    
    def get_current_dir(self):
        return self.currend_dir
    