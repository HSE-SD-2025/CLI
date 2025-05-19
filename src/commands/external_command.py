import subprocess
from typing import List

from src.commands.command_interface import CommandInterface
from src.file_system import FileSystem


class ExternalCommand(CommandInterface):
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
                cwd=self.file_system.get_current_dir()
            )
            print(result.stdout)
            return result.returncode
        except Exception:
            print(f"Command not found: {args[0]}")
            return 1
