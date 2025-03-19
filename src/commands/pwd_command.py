from typing import List
import os
from src.commands.command_interface import CommandInterface

class PwdCommand(CommandInterface):
    def __init__(self):
        super().__init__()

    def execute(self, args: List[str]) -> int:
        print(os.getcwd())
        return 0