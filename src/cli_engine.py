import shlex
from src.commands import commands
from typing import List

from src.commands.external_command import ExternalCommand


class CliEngine:
    def __init__(self):
        self.is_exit = False
        self.return_code = 0

    def __parse_command(self, command_line: str) -> List[str]:
        return shlex.split(command_line)

    def __execute_command(self, parsed_command: List[str]):
        command = commands.commands.get(parsed_command[0], ExternalCommand())
        if isinstance(command, ExternalCommand):
            self.is_exit = command.execute(parsed_command[1:])
        else:
            self.return_code = command.execute(parsed_command[1:])

    def run(self):
        while not self.is_exit:
            input_command = input("> ")
            parsed_command = self.__parse_command(input_command)
            self.__execute_command(parsed_command)
