from typing import List

from src.commands.command_interface import CommandInterface


class ExitCommand(CommandInterface):

    def __init__(self):
        super().__init__()

    def execute(self, args: List[str]) -> bool:
        """
           Leads to normal program termination

           :return: Always return True
           :rtype: bool
           """
        return True
