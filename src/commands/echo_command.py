import sys
from typing import List

from src.commands.command_interface import CommandInterface


class EchoCommand(CommandInterface):
    """
    A command that prints its arguments to stdout, separated by spaces.
    Similar to the Unix echo command.
    """

    def execute(self, args: List[str]) -> int:
        """
        Execute the echo command by printing all arguments to stdout.

        Args:
            args (List[str]): List of arguments to print

        Returns:
            int: 0 if successful, 1 if an error occurred
        """
        try:
            for arg in args:
                print(arg, end=" ")
            return 0
        except Exception as e:
            print(f"echo: An error occurred: {e}", file=sys.stderr)
            return 1
