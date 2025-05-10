from typing import List
from src.file_system import FileSystem

class CommandInterface:
    def __init__(self, file_system: FileSystem):
        self.file_system = file_system
    
    def execute(self, args: List[str]) -> int:
        pass