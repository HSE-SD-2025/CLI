from typing import List
import os
import sys
from src.commands.command_interface import CommandInterface


class CdCommand(CommandInterface):
    """
    A command that changes the current working directory.
    Similar to the Unix cd command.
    """

    def execute(self, args: List[str]) -> int:
        """
        Execute the cd command: change the current directory to the specified path,
        or to the home directory if no path is provided.

        Args:
            args (List[str]): PATH - the directory to change to (optional)

        Returns:
            int: returns 0 if the directory was changed successfully, 1 otherwise
        """
        # Default to home directory if no args provided
        if len(args) == 0:
            path = self.file_system.resolve("~")
        elif len(args) == 1:
            path = self.file_system.resolve(args[0])
        else:
            print("cd: too many arguments", file=sys.stderr)
            return 1

        if not os.path.exists(path):
            print(f"cd: {path}: No such file or directory", file=sys.stderr)
            return 1

        if not os.path.isdir(path):
            print(f"cd: {path}: Not a directory", file=sys.stderr)
            return 1

        if not os.access(path, os.R_OK | os.X_OK):
            print(f"cd: {path}: Permission denied", file=sys.stderr)
            return 1

        try:
            self.file_system.set_current_dir(os.path.abspath(path))
            return 0
        except Exception as e:
            print(f"cd: {path}: {str(e)}", file=sys.stderr)
            return 1
