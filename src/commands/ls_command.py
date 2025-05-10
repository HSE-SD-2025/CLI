from typing import List
import os
import sys
from src.commands.command_interface import CommandInterface

BLUE = "\033[34m"
RESET = "\033[0m"


class LsCommand(CommandInterface):
    """
    A command that list information about the FILE.
    Similar to the Unix ls command.
    """

    def execute(self, args: List[str]) -> int:
        """
        Execute the ls command: list information about the FILE (the current directory by default).

        Args:
            args (List[str]): FILE - the directory or file in which needs to display the contents

        Returns:
            int: returns 0 if the program worked correctly, 1 otherwise
        """
        if len(args) > 1:
            print(f"ls: support only 1 file arguments", file=sys.stderr)
            return 1
        if len(args) == 0:
            path = self.file_system.get_current_dir()
        else:
            path = self.file_system.resolve(args[0])
        if not os.path.exists(path):
            print(f"ls: {path}: No such file or directory", file=sys.stderr)
            return 1
        if os.path.isdir(path):
            for item in os.listdir(path):
                if os.path.isdir(os.path.join(path, item)):
                    print(f"{BLUE}{item}{RESET}")
                print(item)
        else:
            print(path)
        return 0
