import re
import argparse
import sys
from typing import List, Tuple
from src.commands.command_interface import CommandInterface


class GrepCommand(CommandInterface):
    """
    A command that searches for patterns in files, similar to Unix grep.
    Supports regular expressions, word boundaries, case-insensitive search,
    and context lines after matches.
    """

    def __init__(self):
        super().__init__()
        self.parser = argparse.ArgumentParser(prog='grep')
        self.parser.add_argument('pattern', help='Pattern to search for')
        self.parser.add_argument('files', nargs='+', help='Files to search in')
        self.parser.add_argument('-w', '--word-regexp', action='store_true',
                               help='Select only those lines containing matches that form whole words')
        self.parser.add_argument('-i', '--ignore-case', action='store_true',
                               help='Ignore case distinctions')
        self.parser.add_argument('-A', '--after-context', type=int, default=0,
                               help='Print NUM lines of trailing context after matching lines')

    def __parse_args(self, args: List[str]) -> argparse.Namespace:
        """Parse command line arguments"""
        try:
            return self.parser.parse_args(args)
        except argparse.ArgumentError as e:
            print(f"grep: {e}", file=sys.stderr)
            return None

    def __compile_pattern(self, pattern: str, word_regexp: bool, ignore_case: bool) -> re.Pattern:
        """Compile the search pattern with appropriate flags"""
        flags = re.IGNORECASE if ignore_case else 0
        if word_regexp:
            pattern = r'\b' + pattern + r'\b'
        return re.compile(pattern, flags)

    def __process_file(self, file_name: str, pattern: re.Pattern, after_context: int) -> List[Tuple[int, str]]:
        """Process a single file and return matches with their context"""
        matches = []
        try:
            with open(file_name, 'r', encoding='utf-8') as file:
                lines = file.readlines()
                for i, line in enumerate(lines):
                    if pattern.search(line):
                        # Add the matching line
                        matches.append((i, line.rstrip()))
                        # Add context lines if specified
                        for j in range(1, after_context + 1):
                            if i + j < len(lines):
                                matches.append((i + j, lines[i + j].rstrip()))
        except FileNotFoundError:
            print(f"grep: {file_name}: No such file or directory", file=sys.stderr)
        except Exception as e:
            print(f"grep: {file_name}: {e}", file=sys.stderr)
        return matches

    def execute(self, args: List[str]) -> int:
        """
        Execute the grep command by searching for patterns in files.

        Args:
            args (List[str]): Command line arguments including pattern and files

        Returns:
            int: 0 if successful, 1 if an error occurred
        """
        parsed_args = self.__parse_args(args)
        if not parsed_args:
            return 1

        pattern = self.__compile_pattern(
            parsed_args.pattern,
            parsed_args.word_regexp,
            parsed_args.ignore_case
        )

        found_match = False
        for file_name in parsed_args.files:
            matches = self.__process_file(file_name, pattern, parsed_args.after_context)
            if matches:
                found_match = True
                for _, line in matches:
                    print(line)

        return 0 if found_match else 1 