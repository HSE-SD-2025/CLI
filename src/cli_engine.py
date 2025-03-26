import shlex
from typing import List, Optional

from src.commands import commands
from src.commands.exit_command import ExitCommand
from src.commands.external_command import ExternalCommand


class CliEngine:
    def __init__(self):
        self.is_exit = False
        self.return_code = 0

    def __parse_commands(self, command_line: str) -> List[List[str]]:
        """Parse a command line into a list of commands (for pipes)"""
        return [self.__parse_command(cmd) for cmd in command_line.split('|')]

    def __parse_command(self, command: str) -> List[str]:
        """Parse a single command into its components"""
        return shlex.split(command.strip())

    def __execute_piped_commands(self, commands_list: List[List[str]]) -> int:
        """Execute a series of piped commands by chaining them together"""
        if not commands_list:
            return 0

        previous_output = None
        return_code = 0

        for cmd in commands_list:
            if not cmd:
                continue

            command_name = cmd[0]
            args = cmd[1:]

            command = commands.commands.get(command_name, ExternalCommand())

            try:
                if previous_output is not None:
                    if hasattr(command, 'execute_with_input'):
                        result = command.execute_with_input(args, previous_output)
                    else:
                        result = command.execute(args)
                else:
                    result = command.execute(args)

                if isinstance(command, ExitCommand):
                    self.is_exit = result
                    return 0
                previous_output = str(result) if result is not None else ""
                return_code = 0

            except Exception as e:
                print(f"Error executing {command_name}: {str(e)}")
                previous_output = ""
                return_code = 1


        if len(commands_list) == 1 and previous_output:
            print(previous_output, end='')

        return return_code

    def run(self):
        """Run the CLI engine"""
        while not self.is_exit:
            try:
                input_command = input("> ").strip()
                if not input_command:
                    continue

                parsed_commands = self.__parse_commands(input_command)
                self.return_code = self.__execute_piped_commands(parsed_commands)
            except KeyboardInterrupt:
                print("\nUse 'exit' to quit")
                self.return_code = 1
            except Exception as e:
                print(f"Error: {str(e)}")
                self.return_code = 1