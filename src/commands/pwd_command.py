import os
from typing import List

from src.commands.command_interface import CommandInterface


class PwdCommand(CommandInterface):
    """
    A command that prints the current working directory.
    Similar to the Unix pwd command.
    """

    def __init__(self):
        super().__init__()

    def execute(self, args: List[str]) -> int:
        """
        Execute the pwd command by printing the current working directory.

        Args:
            args (List[str]): Not used in this command

        Returns:
            int: Always returns 0 as this command rarely fails
        """
        print(os.getcwd())
        return 0
