import shlex


class CliEngine:
    def __init__(self):
        self.is_exit = False

    def __parse_command(self, command_line: str):
        return shlex.split(command_line)

    def run(self):
        while not self.is_exit:
            input_command = input("> ")
            parsed_command = self.__parse_command(input_command)
