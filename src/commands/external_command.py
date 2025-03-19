from typing import List

from src.commands.command_interface import CommandInterface


class ExternalCommand(CommandInterface):
    def __init__(self):
        super().__init__()

    def execute(self, args: List[str]) -> int:
        pass