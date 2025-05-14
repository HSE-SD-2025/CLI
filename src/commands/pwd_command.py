from typing import List
import os
from src.commands.command_interface import CommandInterface
from src.file_system import FileSystem


class PwdCommand(CommandInterface):
    """
    A command that prints the current working directory.
    Similar to the Unix pwd command.
    """

    def execute(self, args: List[str]) -> int:
        """
        Execute the pwd command by printing the current working directory.

        Args:
            args (List[str]): Not used in this command

        Returns:
            int: Always returns 0 as this command rarely fails
        """
        print(self.file_system.get_current_dir())
        return 0
