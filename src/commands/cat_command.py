import sys
from typing import List

from src.commands.command_interface import CommandInterface


class CatCommand(CommandInterface):

    def execute(self, args: List[str]) -> int:
        if not args:
            try:
                for line in sys.stdin:
                    print(line, end='')
                return 0
            except KeyboardInterrupt:
                print("\nProcess interrupted by user.")
                return 1
            except Exception as e:
                print(f"Error reading from stdin: {e}", file=sys.stderr)
                return 1
        for file_name in args:
            try:
                with open(file_name, 'r') as file:
                    for line in file:
                        print(line, end='')
            except FileNotFoundError:
                print(f"cat: {file_name}: No such file or directory", file=sys.stderr)
                return 1
            except PermissionError:
                print(f"cat: {file_name}: Permission denied", file=sys.stderr)
                return 1
            except Exception as e:
                print(f"cat: {file_name}: {e}", file=sys.stderr)
                return 1

        return 0