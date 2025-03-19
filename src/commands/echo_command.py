import sys
from typing import List

from src.commands.command_interface import CommandInterface


class EchoCommand(CommandInterface):

    def execute(self, args: List[str]) -> int:
        try:
            for arg in args:
                print(arg)
            return 0
        except Exception as e:
            print(f"echo: An error occurred: {e}", file=sys.stderr)
            return 1
