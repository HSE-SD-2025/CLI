import os
from typing import List

from src.commands.command_interface import CommandInterface


class WcCommand(CommandInterface):

    def __init__(self):
        super().__init__()

    def __print_stats(self, lines, words, bytes_count, name=""):
        if name:
            print(f"{lines:8} {words:8} {bytes_count:7} {name}")
        else:
            print(f"{lines:8} {words:8} {bytes_count:7}")

    """
    Outputs the number of lines, words, and bytes for each specified file
    and a summary line if multiple files were specified.
    
    :param List[str] args: list of files for which the command will be called
    :return: returns 0 if the program worked correctly, 1 otherwise
    :rtype: int
    """

    def execute(self, args: List[str]) -> int:
        code = 0
        files = args
        total_lines = total_words = total_bytes = 0
        for file_name in files:
            try:
                with open(file_name, 'r', encoding='utf-8') as f:
                    content = f.read()
            except FileNotFoundError:
                print(f"wc: {file_name}: No such file or directory")
                code = 1
                continue
            lines = content.count(os.linesep)
            words = len(content.split())
            bytes_count = len(content.encode('utf-8'))
            self.__print_stats(lines, words, bytes_count, file_name)
            total_lines += lines
            total_words += words
            total_bytes += bytes_count

        if len(files) > 1:
            self.__print_stats(total_lines, total_words, total_bytes, "total")

        return code
