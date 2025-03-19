from typing import List

from src.commands.command_interface import CommandInterface


class WcCommand(CommandInterface):

    def __init__(self):
        super().__init__()

    """
    Leads to normal program termination

    :return: Always return True
    :rtype: bool
    """

    def execute(self, args: List[str]) -> bool:
        return True
