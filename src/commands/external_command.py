import subprocess
from typing import List

from src.commands.command_interface import CommandInterface


class ExternalCommand(CommandInterface):
    def __init__(self):
        super().__init__()

    def execute(self, args: List[str]) -> int:
        """Execute external command
        :param List[str] args: program name and list of arguments
        :return: Return code of the executed command or 1 if command not found
        :rtype: bool
        """
        try:
            result = subprocess.run(
                args,
                capture_output=True,
                text=True,
            )
            print(result.stdout)
            return result.returncode
        except Exception:
            print(f"Command not found: {args[0]}")
            return 1
